"""Super Refactoring Intelligence — governed observe/measure/propose."""
__all__ = ["run", "RefactorReport", "SuperRefactorEngine"]

def __getattr__(name: str):
    if name in ("run", "RefactorReport"):
        from . import super_refactor as m
        return getattr(m, name)
    if name == "SuperRefactorEngine":
        from .super_refactor import run as _run
        class SuperRefactorEngine:
            """Thin facade: observe → measure → propose (no auto-merge)."""
            def run(self, submit: bool = False, ingest_sources: bool = False):
                return _run(submit=submit, ingest_sources=ingest_sources)
        return SuperRefactorEngine
    raise AttributeError(name)
