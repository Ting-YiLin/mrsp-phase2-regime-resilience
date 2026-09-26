from pathlib import Path
import csv, json, math, re
root=Path(__file__).resolve().parents[1]
exp=json.loads((root/'evidence'/'EXPECTED_KEY_RESULTS.json').read_text())

def rows(name):
    with (root/'data'/name).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))

def one(rs, **kw):
    m=[r for r in rs if all(str(r[k])==str(v) for k,v in kw.items())]
    if len(m)!=1: raise AssertionError((kw,len(m)))
    return m[0]

def close(a,b,tol=2e-6):
    if not math.isclose(float(a),float(b),abs_tol=tol): raise AssertionError((a,b))

p1=rows('P1_ACCURACY_COVERAGE_FRONTIER.csv')
sig=rows('REGIME_SIGNAL_COUNT_MAP.csv')
cross=rows('CROSS_DOMAIN_SUMMARY.csv')
close(one(p1,cohort='REPRESENTATIVE',p1_tier='ALL')['v1_accuracy'], exp['representative_all_v1_accuracy'])
close(one(p1,cohort='REPRESENTATIVE',p1_tier='ALL')['d28_accuracy'], exp['representative_all_d28_accuracy'])
close(one(p1,cohort='DEPARTMENT_CHALLENGE',p1_tier='ALL')['v1_accuracy'], exp['department_all_v1_accuracy'])
close(one(p1,cohort='DEPARTMENT_CHALLENGE',p1_tier='ALL')['d28_accuracy'], exp['department_all_d28_accuracy'])
close(one(sig,cohort='REPRESENTATIVE',signal_stratum='3')['accuracy_delta_pp'], exp['representative_signal3_delta_pp'])
close(one(sig,cohort='DEPARTMENT_CHALLENGE',signal_stratum='3')['accuracy_delta_pp'], exp['department_signal3_delta_pp'])
close(one(sig,cohort='REPRESENTATIVE',signal_stratum='3')['coverage_of_cohort'], exp['representative_signal3_coverage'])
close(one(sig,cohort='DEPARTMENT_CHALLENGE',signal_stratum='3')['coverage_of_cohort'], exp['department_signal3_coverage'])
close(one(cross,result='H&M frozen V1 external replication')['accuracy'], exp['hm_v1_accuracy'])
close(one(cross,result='H&M D28 development')['accuracy'], exp['hm_d28_accuracy'], 3e-6)

required=['README.md','ARTICLE.md','ARTICLE_zh-TW.md','CLAIMS.md','RIGHTS_NOTICE.md','technical/TECHNICAL_APPENDIX.md','paper/MRSP_Phase2_When_History_Stops_Working.pdf','figures/figure_1_accuracy_coverage_frontier.png','figures/figure_2_hm_coverage_collapse.png','figures/figure_3_cross_domain_d28_effect.png','figures/figure_4_regime_rescue_by_signal_count.png','figures/figure_5_operational_map.png','data/FULL_P1_X_SIGNAL_FRONTIER.csv']
missing=[x for x in required if not (root/x).exists()]
if missing: raise AssertionError('missing '+repr(missing))

# Claim-evidence paths must resolve exactly with public case-sensitive paths.
with (root/'evidence'/'CLAIM_EVIDENCE_LEDGER.csv').open(newline='',encoding='utf-8') as f:
    claims=list(csv.DictReader(f))
if len(claims)!=12: raise AssertionError(('claims',len(claims)))
for r in claims:
    for rel in [x.strip() for x in r['direct_evidence'].split(';') if x.strip()]:
        if not (root/rel).is_file(): raise AssertionError(('broken_direct_evidence',r['claim_id'],rel))
if one(claims,claim_id='C10')['direct_evidence']!='data/FULL_P1_X_SIGNAL_FRONTIER.csv':
    raise AssertionError('C10 evidence path unexpected')

# Uncertainty table must have unique semantic keys; final R13 product-set bootstrap is frozen.
unc=rows('UNCERTAINTY_SUMMARY.csv')
keys=[(r['cohort'],r['stratum'],r['cluster_unit']) for r in unc]
if len(keys)!=len(set(keys)): raise AssertionError('duplicate uncertainty semantic key')
u=one(unc,cohort='Department Challenge',stratum='HIGH_SHOCK',cluster_unit='product_set')
close(u['mean_delta_pp'],1.4859802463703586,1e-12)
close(u['ci95_low_pp'],0.11471029161528438,1e-12)
close(u['ci95_high_pp'],3.1105161758816426,1e-12)

# Public navigation and platform readback metadata.
texts=[]
for rel in ['README.md','ARTICLE.md','PUBLICATION_METADATA.yaml']:
    texts.append((root/rel).read_text(encoding='utf-8'))
joined='\n'.join(texts)
if 'zenodo.org/uploads/22969898' in joined: raise AssertionError('draft Zenodo URL remains')
if 'https://zenodo.org/records/22969898' not in joined: raise AssertionError('published Zenodo record URL missing')
meta=(root/'PUBLICATION_METADATA.yaml').read_text(encoding='utf-8')
for token in ['abstract_id: "7526699"','submission_status: "PRELIMINARY_UPLOAD"','submission_id: null']:
    if token not in meta: raise AssertionError(('metadata token missing',token))
if 'RETURN_AFTER_SUBMISSION' in meta: raise AssertionError('SSRN placeholder remains')

check=(root/'audit'/'PUBLIC_CLAIM_CHECKLIST.md').read_text(encoding='utf-8')
if '- [ ]' in check: raise AssertionError('unchecked public claim item remains')
if (root/'RELEASE_VERSION').read_text(encoding='utf-8').strip()!='1.0.1': raise AssertionError('release version')

print('PUBLIC_RELEASE_VERIFY_PASS claims=12 figures=5 key_results=10 traceability=PASS uncertainty_unique=PASS round2=PASS')
