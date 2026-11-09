from pathlib import Path
from .project import ProjectStore, validate_pack_pair
from .rule_packs import RulePackStore
from textmarker.da_interference import scan_and_write
from textmarker.da_interference import DARule

def scan_project(profile_path, source, output, report, summary=None, pack_root=None, cancel=None, progress=None):
    profile=ProjectStore(profile_path).load(); packs=RulePackStore(pack_root or Path(profile_path).parent/'rule_packs'); available={p.stem for p in packs.list()}; active=ProjectStore(profile_path).valid_rule_packs(available)
    if not active: raise ValueError('Projektet har ingen tilgængelige aktive rule packs')
    if len(active)!=len(profile.rule_pack_ids): raise ValueError('Projektet refererer til manglende rule packs')
    merged=[]; seen={}
    for pack_id in sorted(active):
        pack=packs.load(pack_id); validate_pack_pair(pack,profile.source_language,profile.target_language)
        for rule in pack.rules:
            if rule.rule_id in seen:
                previous=seen[rule.rule_id]
                if previous != rule: raise ValueError(f'Konfliktende rule ID på tværs af packs: {rule.rule_id}')
                continue
            seen[rule.rule_id]=rule
            merged.append(DARule(rule.expression,rule.category,rule.category.casefold(),rule.severity,rule.explanation,rule.suggested_review,rule.enabled,len(merged),rule.rule_id))
    return scan_and_write(source,merged,output,report,summary_path=summary,cancel=cancel,progress=progress)
