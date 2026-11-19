"""
Niyete bağlı yetenek belirteçleri (Intent-Bound Capability Tokens) — VERIQEN 2.0, özellik 1.

Fikir: Kullanıcının isteği, sınırlı ve tek kullanımlık işlem yetkilerine (belirteç) dönüştürülür.
Ajanın hassas bir çağrısı bir belirtece TAM uyuyorsa hakem çağrılmadan yürütülür ve belirteç tüketilir;
uymuyorsa pahalı doğrulamaya (hakem) gider. Belirteç yalnızca iki güvenilir kaynaktan üretilir:

  1. Kullanıcı isteğinde açıkça yazılmış IBAN'lar.
  2. Kullanıcının isteğinde ADIYLA andığı bir alıcı ("Spotify", "Apple", "rent"): bu ad, yalnızca
     kullanıcının KENDİ başlattığı işlemlerin (gönderen = kullanıcı) konu alanlarında aranır ve eşleşen
     işlemin alıcısına çözülür. Gelen transferler (gönderen = başkası) aranmaz; çünkü onların konu ve
     gönderen alanlarını dışarıdaki biri yazar (durum ekme saldırısı, 12 §3b).

Araç çıktıları (dosya, fatura, işlem açıklaması) hiçbir zaman belirteç üretemez.

Belirteç alanları: işlem türleri, alıcı, azami tutar, kalan kullanım, bölüm (geçerlilik), imza.
  * Kullanım sayısı varsayılan 1: kullanıcının bir kez andığı alıcıya, hakem çağrılmadan bir hassas işlem.
    Aynı alıcıya ikinci işlem hakeme gider ("doğru alıcıya istenmemiş ek işlem" açığı, 12 §3c).
  * Geçerlilik bölümle sınırlı: yeni bir kullanıcı isteğinde eski belirteçler geçersizdir.
  * İmza: HMAC-SHA256, oturum başına rastgele anahtar. Tek süreçli deneyde belirteç bir güven sınırını
    aşmadığı için imzanın güvenlik katkısı YOKTUR; ürün mimarisinde (belirteci üreten bileşen ile
    uygulayan bileşen ayrıysa) anlamlıdır. Testlerde kurcalamaya karşı doğrulanır.

Literatürle ilişki: Yetenek tabanlı yetkilendirme yeni değildir (CaMeL'in değerlere bağlı yetenekleri,
Progent'in ayrıcalık politikaları, Macaroons). Buradaki soru, bu yapının YÖNLENDİRMEDE hakemin yerine
geçtiğinde güvenlik / yanlış engelleme / maliyet dengesine etkisidir.
"""
from __future__ import annotations

import hashlib
import hmac
import itertools
import json
import re
import secrets
from dataclasses import asdict, dataclass, field
from typing import Any

IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b")
_WORD_RE = re.compile(r"[a-z][a-z0-9]{3,}")

# Ad eşleştirmede yok sayılan genel kelimeler. Liste görev metinlerinden değil, genel İngilizce ve
# bankacılık sözcüklerinden oluşturuldu; yine de dev kümesi görülerek yazıldığı not edilmelidir.
STOPWORDS = frozenset("""
please could would should will them they their there that this these those with from what which have
about make sure also just send sent sending money account accounts accordingly read file files payment
payments transaction transactions month months last next like check update updated adjust amount
amounts total much more after before into your mine have been were was when where here only need needs
want wants usually pay paid paying refund transfer recurring scheduled schedule set setup subscription
service note difference history increased increase price prices percent called said include included
year years week weeks today recent finally just been things something little bit
""".split())

ID_SEP = "|"


def _norm(s: Any) -> str:
    return str(s).strip().lower()


@dataclass
class CapabilityToken:
    token_id: str
    operations: tuple[str, ...]        # izin verilen hassas araçlar
    recipient: str                     # normalize edilmiş IBAN
    max_amount: float
    uses_left: int
    episode: int
    source: str                        # "user_iban" | "named_payee:<ad>"
    signature: str = ""

    def payload(self) -> bytes:
        d = asdict(self); d.pop("signature")
        return json.dumps(d, sort_keys=True).encode()


@dataclass
class TokenStore:
    key: bytes = field(default_factory=lambda: secrets.token_bytes(32))
    tokens: list[CapabilityToken] = field(default_factory=list)
    episode: int = 0
    _ids: Any = field(default_factory=lambda: itertools.count(1))

    # --- imza ---
    def _sign(self, t: CapabilityToken) -> str:
        return hmac.new(self.key, t.payload(), hashlib.sha256).hexdigest()

    def verify(self, t: CapabilityToken) -> bool:
        return bool(t.signature) and hmac.compare_digest(t.signature, self._sign(t))

    def _resign(self, t: CapabilityToken) -> None:
        t.signature = self._sign(t)

    # --- yaşam döngüsü ---
    def new_episode(self) -> None:
        """Yeni kullanıcı isteği: önceki bölümün belirteçleri geçersiz olur."""
        self.episode += 1
        self.tokens = []

    def issue(self, operations, recipient: str, max_amount: float, source: str, uses: int = 1) -> CapabilityToken:
        t = CapabilityToken(token_id=f"cap-{self.episode}-{next(self._ids)}", operations=tuple(sorted(operations)),
                            recipient=_norm(recipient), max_amount=float(max_amount), uses_left=int(uses),
                            episode=self.episode, source=source)
        self._resign(t)
        self.tokens.append(t)
        return t

    # --- eşleştirme ---
    def match(self, operation: str, recipient: Any, amount: float | None) -> tuple[CapabilityToken | None, str]:
        """Çağrıya tam uyan, geçerli bir belirteç arar. (belirteç, neden) döndürür; belirteç yoksa neden açıklar."""
        if recipient is None:
            return None, "cap:no_recipient"
        rcpt = _norm(recipient)
        reasons = []
        for t in self.tokens:
            if t.recipient != rcpt:
                continue
            if not self.verify(t):
                reasons.append("cap:bad_signature"); continue
            if t.episode != self.episode:
                reasons.append("cap:expired"); continue
            if operation not in t.operations:
                reasons.append("cap:operation_not_granted"); continue
            if t.uses_left <= 0:
                reasons.append("cap:used_up"); continue
            if amount is not None and float(amount) > t.max_amount:
                reasons.append("cap:amount_over_limit"); continue
            return t, f"cap:{t.token_id}"
        return None, (reasons[0] if reasons else "cap:no_token_for_recipient")

    def consume(self, t: CapabilityToken) -> None:
        t.uses_left -= 1
        self._resign(t)


# ---------------------------------------------------------------------------
# Belirteç üretimi (yalnız güvenilir kaynaklardan)
# ---------------------------------------------------------------------------
def prompt_ibans(user_prompt: str) -> set[str]:
    return {_norm(m) for m in IBAN_RE.findall(user_prompt or "")}


def named_payees(user_prompt: str, env) -> dict[str, str]:
    """Kullanıcının adıyla andığı alıcıları, kullanıcının KENDİ başlattığı işlemlerden çözer.
    {alıcı_iban: eşleşen_ad} döndürür."""
    acct = env.bank_account
    own = {_norm(acct.iban), "me"}
    words = {w for w in _WORD_RE.findall((user_prompt or "").lower()) if w not in STOPWORDS}
    out: dict[str, str] = {}
    for t in list(acct.transactions) + list(acct.scheduled_transactions):
        if _norm(t.sender) not in own:              # gelen transfer: konusunu başkası yazdı
            continue
        subj = set(_WORD_RE.findall(str(t.subject or "").lower()))
        hit = sorted(words & subj)
        if hit:
            out.setdefault(_norm(t.recipient), hit[0])
    return out


def mint_tokens(store: TokenStore, user_prompt: str, env, allowed_operations: set[str], money_tools: set[str],
                max_amount: float, named: bool = False) -> list[CapabilityToken]:
    """İzinli hassas para işlemleri × güvenilir alıcılar için tek kullanımlık belirteçler üretir.

    named=True, adıyla anılan alıcıları da (kullanıcının kendi geçmiş işlemlerinden) çözer. Val kümesinde
    bu seçeneğin fazla izin verdiği görüldü: bir alıcının adının geçmesi, ona ödeme yapma niyeti değildir
    (ör. "yeni ev sahibime geçir" isteğinde eski ev sahibinin 'Rent' kaydı da belirteç alıyor). Bu yüzden
    varsayılan kapalı; VERIQEN-TN sürümünde olumsuz sonuç olarak raporlanır."""
    ops = tuple(sorted(set(allowed_operations) & set(money_tools)))
    if not ops:
        return []
    issued = []
    for iban in sorted(prompt_ibans(user_prompt)):
        issued.append(store.issue(ops, iban, max_amount, "user_iban"))
    if not named:
        return issued
    for iban, name in sorted(named_payees(user_prompt, env).items()):
        if any(t.recipient == iban for t in issued):
            continue
        issued.append(store.issue(ops, iban, max_amount, f"named_payee:{name}"))
    return issued
