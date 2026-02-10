from ..base import resolve_id
from catweek.db.models import specialties

def resolve_specialty_id(conn, specialty_name: str) -> int:
    resolved_specialty = resolve_id(
        conn,
        specialties,
        specialties.c.specialty_id,
        where={"specialty_name": specialty_name},
        label=f"specialty '{specialty_name}'",
    )
    return resolved_specialty