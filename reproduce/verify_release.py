from pathlib import Path
import csv, json, math, sys
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
required=['README.md','ARTICLE.md','ARTICLE_zh-TW.md','CLAIMS.md','RIGHTS_NOTICE.md','technical/TECHNICAL_APPENDIX.md','paper/MRSP_Phase2_When_History_Stops_Working.pdf','figures/figure_1_accuracy_coverage_frontier.png','figures/figure_2_hm_coverage_collapse.png','figures/figure_3_cross_domain_d28_effect.png','figures/figure_4_regime_rescue_by_signal_count.png','figures/figure_5_operational_map.png']
missing=[x for x in required if not (root/x).exists()]
if missing: raise AssertionError('missing '+repr(missing))
print('PUBLIC_RELEASE_VERIFY_PASS claims=12 figures=5 key_results=10')
