from pathlib import Path
from .project import ProjectStore, validate_pack_pair
from .rule_packs import RulePackStore
from textmarker.da_interference import scan_and_write

def scan_project(profile_path, source, output, report, summary=None, pack_root=None, cancel=None, progress=None):
    profile=ProjectStore(profile_path).load(); packs=RulePackStore(pack_root or Path(profile_path).parent/'rule_packs'); available={p.stem for p in packs.list()}; active=ProjectStore(profile_path).valid_rule_packs(available)
    if not active: raise ValueError('Projektet har ingen tilgængelige aktive rule packs')
    if len(active)!=len(profile.rule_pack_ids): raise ValueError('Projektet refererer til manglende rule packs')
    pack=packs.load(active[0]); validate_pack_pair(pack,profile.source_language,profile.target_language)
    return scan_and_write(source,pack.rules,output,report,summary_path=summary,cancel=cancel,progress=progress)
