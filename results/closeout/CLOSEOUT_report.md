# Close-out report

Mode: test. Not confirmed means the test-session point estimate failed the frozen check. With five sessions this is not a refutation of the discovery result and not evidence for the opposite claim. VIP0 is the only attainable schedule; every other is hypothetical.

## Run history

- authorised 1: ledger_commit=6fd7d2b7e282, freeze_record_sha256=2e81527f73c3aff00f7a3c049b3104fe5ac6e211e702b7158480979c2be056ee, utc=2026-11-05T00:06:10+00:00
- started 1: ledger_commit=c5aba78f70ba
- completed 1: ledger_commit=2447d2a270c7

Undefined sessions (section 1's input rule; they leave every check): none

Sessions with no valid unit in an experiment (not undefined): none

Test relative tick (bp), against 0.46–1.20 bp on discovery; applies to every bp result below; δ thresholds are not rescaled: {'2026-06-01': 1.2326300573288953, '2026-07-01': 1.3178565431327423, '2026-08-01': 1.3784104217724051, '2026-09-01': 0.981656517292535, '2026-10-01': 0.8468836764887745}

## E001

State: complete. Status: observed.

one family (rs = es - 2 mo)

Tally (not independent replications): 6 of 6 confirmed.

| Check | Label | Discovery | Test | Status | Notes | Flag |
|---|---|---|---|---|---|---|
| E001 mo_1s | **confirmed (point estimate, 5 of 5 defined)** | 0.9853312268303135 | mo_1s: mean 0.8496; 5 defined, 5 +, 0 −; t-interval (descriptive, not used) ['0.6314', '1.068']; sessions 2026-06-01: 0.8435, 2026-07-01: 1.137, 2026-08-01: 0.6771, 2026-09-01: 0.8457, 2026-10-01: 0.7445 | observed | mean of session means has the discovery sign, and that sign holds in at least 4 of 5 sessions; sign_count: 5 |  |
| E001 mo_5s | **confirmed (point estimate, 5 of 5 defined)** | 1.100595332654191 | mo_5s: mean 0.9503; 5 defined, 5 +, 0 −; t-interval (descriptive, not used) ['0.7505', '1.15']; sessions 2026-06-01: 1.02, 2026-07-01: 1.178, 2026-08-01: 0.7591, 2026-09-01: 0.9464, 2026-10-01: 0.8484 | observed | mean of session means has the discovery sign, and that sign holds in at least 4 of 5 sessions; sign_count: 5 |  |
| E001 mo_30s | **confirmed (point estimate, 5 of 5 defined)** | 1.167127869658535 | mo_30s: mean 1.006; 5 defined, 5 +, 0 −; t-interval (descriptive, not used) ['0.8043', '1.208']; sessions 2026-06-01: 1.108, 2026-07-01: 1.229, 2026-08-01: 0.8473, 2026-09-01: 0.9843, 2026-10-01: 0.8636 | observed | mean of session means has the discovery sign, and that sign holds in at least 4 of 5 sessions; sign_count: 5 |  |
| E001 rs_1s | **confirmed (point estimate, 5 of 5 defined)** | -0.6949743744803417 | rs_1s: mean -0.2778; 5 defined, 1 +, 4 −; t-interval (descriptive, not used) ['-0.7747', '0.2191']; sessions 2026-06-01: -0.2031, 2026-07-01: -0.7541, 2026-08-01: 0.342, 2026-09-01: -0.377, 2026-10-01: -0.3969 | observed | mean of session means has the discovery sign, and that sign holds in at least 4 of 5 sessions; sign_count: 4 |  |
| E001 rs_5s | **confirmed (point estimate, 5 of 5 defined)** | -0.925502586128097 | rs_5s: mean -0.4794; 5 defined, 1 +, 4 −; t-interval (descriptive, not used) ['-0.9566', '-0.002141']; sessions 2026-06-01: -0.5551, 2026-07-01: -0.8365, 2026-08-01: 0.178, 2026-09-01: -0.5785, 2026-10-01: -0.6048 | observed | mean of session means has the discovery sign, and that sign holds in at least 4 of 5 sessions; sign_count: 4 |  |
| E001 rs_30s | **confirmed (point estimate, 5 of 5 defined)** | -1.0585676601367848 | rs_30s: mean -0.5914; 5 defined, 1 +, 4 −; t-interval (descriptive, not used) ['-1.029', '-0.1537']; sessions 2026-06-01: -0.7318, 2026-07-01: -0.9373, 2026-08-01: 0.001651, 2026-09-01: -0.6542, 2026-10-01: -0.6352 | observed | mean of session means has the discovery sign, and that sign holds in at least 4 of 5 sessions; sign_count: 4 |  |

es (reported only, no confirmatory weight):

| Check | Label | Discovery | Test | Status | Notes | Flag |
|---|---|---|---|---|---|---|
| E001 es | **reported only (point estimate, 5 of 5 defined)** | 1.2756880791802852 | es: mean 1.421; 5 defined, 5 +, 0 −; t-interval (descriptive, not used) ['1.137', '1.705']; sessions 2026-06-01: 1.484, 2026-07-01: 1.52, 2026-08-01: 1.696, 2026-09-01: 1.314, 2026-10-01: 1.092 | observed | mean of session means has the discovery sign, and that sign holds in at least 4 of 5 sessions; Close to mechanical for aggressive trades; no confirmatory weight.; sign_count: 5; same_test_no_weight: sign rule holds |  |

| Item (reported only) | Discovery | Test |
|---|---|---|
| descriptive.pre_state_age_ms_quantiles.exchange (primary).0.5 | 50.81 | 54.561 |
| descriptive.pre_state_age_ms_quantiles.exchange (primary).0.9 | 95.095 | 137.489 |
| descriptive.pre_state_age_ms_quantiles.exchange (primary).0.99 | 251.873 | 443.021 |
| descriptive.pre_state_age_ms_quantiles.receipt+0ms.0.5 | 55.711 | 58.852 |
| descriptive.pre_state_age_ms_quantiles.receipt+0ms.0.9 | 100.565 | 147.243 |
| descriptive.pre_state_age_ms_quantiles.receipt+0ms.0.99 | 255.756 | 471.52 |
| descriptive.pre_state_age_ms_quantiles.receipt+200ms.0.5 | 255.844 | 260.698 |
| descriptive.pre_state_age_ms_quantiles.receipt+200ms.0.9 | 300.691 | 360.367 |
| descriptive.pre_state_age_ms_quantiles.receipt+200ms.0.99 | 469.199 | 683.181 |
| descriptive.pre_state_age_ms_quantiles.receipt+50ms.0.5 | 103.91 | 112.795 |
| descriptive.pre_state_age_ms_quantiles.receipt+50ms.0.9 | 148.031 | 205.531 |
| descriptive.pre_state_age_ms_quantiles.receipt+50ms.0.99 | 310.243 | 530.988 |
| descriptive.secondary_horizons[mo_0.1s].events | 4134210 | 720889 |
| descriptive.secondary_horizons[mo_0.1s].mean_of_session_means | 0.5966936850170496 | 0.5652355012614334 |
| descriptive.secondary_horizons[rs_0.1s].events | 4134210 | 720889 |
| descriptive.secondary_horizons[rs_0.1s].mean_of_session_means | 0.08178466477611762 | 0.29034498343203896 |
| descriptive.secondary_horizons[mo_60s].events | 4114986 | 719256 |
| descriptive.secondary_horizons[mo_60s].mean_of_session_means | 1.168125553411362 | 0.9846052129979043 |
| descriptive.secondary_horizons[rs_60s].events | 4114986 | 719256 |
| descriptive.secondary_horizons[rs_60s].mean_of_session_means | -1.0604740991493253 | -0.5478050924913775 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/es].event_weighted_mean | 1.2981626627047125 | 1.3959146427848321 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/es].events | 4120728 | 720066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/es].mean_of_session_means | 1.2756880791802852 | 1.421297260156206 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/es].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/es].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_1s].event_weighted_mean | 1.0511504215155254 | 0.8884731866953005 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_1s].events | 4120728 | 720066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_1s].mean_of_session_means | 0.9853312268303135 | 0.8495563617275075 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_1s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_5s].event_weighted_mean | 1.1648979715812606 | 0.9847806215802167 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_5s].events | 4120728 | 720066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_5s].mean_of_session_means | 1.100595332654191 | 0.950346001959705 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_5s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_30s].event_weighted_mean | 1.2113175834166825 | 1.035802562175248 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_30s].events | 4120728 | 720066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_30s].mean_of_session_means | 1.167127869658535 | 1.006330049731746 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/mo_30s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_1s].event_weighted_mean | -0.8041381803263382 | -0.38103173060576884 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_1s].events | 4120728 | 720066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_1s].mean_of_session_means | -0.6949743744803417 | -0.2778154632988091 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_1s].sessions_positive | 1 | 1 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_5s].event_weighted_mean | -1.0316332804578083 | -0.5736466003756019 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_5s].events | 4120728 | 720066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_5s].mean_of_session_means | -0.925502586128097 | -0.4793947437632041 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_5s].sessions_positive | 1 | 1 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_30s].event_weighted_mean | -1.1244725041286525 | -0.6756904815656638 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_30s].events | 4120728 | 720066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_30s].mean_of_session_means | -1.0585676601367848 | -0.5913628393072864 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/all/rs_30s].sessions_positive | 0 | 1 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/es].event_weighted_mean | 1.6543644566650444 | 1.6133077126010291 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/es].events | 1456489 | 284371 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/es].mean_of_session_means | 1.602416952606571 | 1.6404770207711965 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/es].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/es].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_1s].event_weighted_mean | 1.6354888667628835 | 1.3920863026437356 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_1s].events | 1456489 | 284371 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_1s].mean_of_session_means | 1.57684243666919 | 1.3554311144950764 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_1s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_5s].event_weighted_mean | 1.7849015791819887 | 1.4987084572045117 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_5s].events | 1456489 | 284371 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_5s].mean_of_session_means | 1.7304752829204906 | 1.4783793190979855 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_5s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_30s].event_weighted_mean | 1.8020893969516876 | 1.5047626676494497 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_30s].events | 1456489 | 284371 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_30s].mean_of_session_means | 1.7779341403062385 | 1.5244520041496679 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/mo_30s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_1s].event_weighted_mean | -1.6166132768607224 | -1.170864892686442 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_1s].events | 1456489 | 284371 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_1s].mean_of_session_means | -1.5512679207318085 | -1.0703852082189558 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_1s].sessions_positive | 0 | 0 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_5s].event_weighted_mean | -1.9154387016989332 | -1.3841092018079946 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_5s].events | 1456489 | 284371 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_5s].mean_of_session_means | -1.8585336132344104 | -1.316281617424774 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_5s].sessions_positive | 0 | 0 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_30s].event_weighted_mean | -1.94981433723833 | -1.39621762269787 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_30s].events | 1456489 | 284371 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_30s].mean_of_session_means | -1.9534513280059058 | -1.4084269875281392 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=L/rs_30s].sessions_positive | 0 | 0 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/es].event_weighted_mean | 1.15432564790561 | 1.2460580874606815 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/es].events | 1393365 | 232629 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/es].mean_of_session_means | 1.0999129865515103 | 1.2691594049622756 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/es].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/es].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_1s].event_weighted_mean | 0.8397678823250175 | 0.6701820100481605 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_1s].events | 1393365 | 232629 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_1s].mean_of_session_means | 0.7464345833473588 | 0.6194694221914983 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_1s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_5s].event_weighted_mean | 0.9679026478373569 | 0.7679903845128927 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_5s].events | 1393365 | 232629 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_5s].mean_of_session_means | 0.871458645364933 | 0.7141192902026029 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_5s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_30s].event_weighted_mean | 1.015038374744148 | 0.8433844080086542 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_30s].events | 1393365 | 232629 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_30s].mean_of_session_means | 0.9372109580263172 | 0.7882693760024546 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/mo_30s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_1s].event_weighted_mean | -0.5252101167444245 | -0.09430593263563954 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_1s].events | 1393365 | 232629 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_1s].mean_of_session_means | -0.39295618014320716 | 0.030220560579279167 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_1s].sessions_positive | 4 | 2 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_5s].event_weighted_mean | -0.7814796477691035 | -0.2899226815651041 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_5s].events | 1393365 | 232629 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_5s].mean_of_session_means | -0.6430043041783559 | -0.15907917544293015 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_5s].sessions_positive | 1 | 1 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_30s].event_weighted_mean | -0.875751101582686 | -0.44071072855662724 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_30s].events | 1393365 | 232629 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_30s].mean_of_session_means | -0.7745089295011243 | -0.30737934704263353 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=M/rs_30s].sessions_positive | 1 | 1 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/es].event_weighted_mean | 1.047637014561829 | 1.2631533531144787 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/es].events | 1270874 | 203066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/es].mean_of_session_means | 1.0381082639732464 | 1.2953968949283519 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/es].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/es].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_1s].event_weighted_mean | 0.61322385597032 | 0.4332905994422646 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_1s].events | 1270874 | 203066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_1s].mean_of_session_means | 0.5288621614168749 | 0.4102608757626595 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_1s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_5s].event_weighted_mean | 0.6703233362024951 | 0.5134339831199046 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_5s].events | 1270874 | 203066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_5s].mean_of_session_means | 0.5820612030530664 | 0.4899288276689573 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_5s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_30s].event_weighted_mean | 0.7494589976467477 | 0.5995079024676473 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_30s].events | 1270874 | 203066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_30s].mean_of_session_means | 0.6601658378378673 | 0.5509156764003992 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/mo_30s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_1s].event_weighted_mean | -0.1788106973788108 | 0.3965721542299495 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_1s].events | 1270874 | 203066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_1s].mean_of_session_means | -0.019616058860503254 | 0.47487514340303294 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_1s].sessions_positive | 6 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_5s].event_weighted_mean | -0.2930096578431608 | 0.23628538687466974 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_5s].events | 1270874 | 203066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_5s].mean_of_session_means | -0.12601414213288636 | 0.31553923959043734 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_5s].sessions_positive | 5 | 4 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_30s].event_weighted_mean | -0.4512809807316664 | 0.06413754817918449 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_30s].events | 1270874 | 203066 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_30s].mean_of_session_means | -0.28222341170248844 | 0.1935655421275538 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/size=S/rs_30s].sessions_positive | 5 | 2 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/es].event_weighted_mean | 0.8596704654440573 | 0.8975621710556516 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/es].events | 905189 | 149809 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/es].mean_of_session_means | 0.885905684214812 | 0.9394685882172308 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/es].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/es].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_1s].event_weighted_mean | 0.3192505989183608 | 0.055281650250099026 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_1s].events | 905189 | 149809 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_1s].mean_of_session_means | 0.3079449374820283 | 0.05733422570853508 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_1s].sessions_positive | 15 | 4 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_5s].event_weighted_mean | 0.21690306735401943 | -0.021844630480609854 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_5s].events | 905189 | 149809 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_5s].mean_of_session_means | 0.19199507947229374 | -0.020640124122470026 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_5s].sessions_positive | 13 | 2 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_30s].event_weighted_mean | 0.15202895014327658 | -0.0902775295768749 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_30s].events | 905189 | 149809 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_30s].mean_of_session_means | 0.12749911826381857 | -0.07840511699308449 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/mo_30s].sessions_positive | 11 | 2 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_1s].event_weighted_mean | 0.22116926760733568 | 0.7869988705554537 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_1s].events | 905189 | 149809 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_1s].mean_of_session_means | 0.27001580925075547 | 0.8248001368001606 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_1s].sessions_positive | 13 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_5s].event_weighted_mean | 0.4258643307360184 | 0.9412514320168713 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_5s].events | 905189 | 149809 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_5s].mean_of_session_means | 0.5019155252702246 | 0.9807488364621706 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_5s].sessions_positive | 13 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_30s].event_weighted_mean | 0.5556125651575041 | 1.0781172302094015 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_30s].events | 905189 | 149809 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_30s].mean_of_session_means | 0.6309074476871749 | 1.0962788222033997 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=against/rs_30s].sessions_positive | 13 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/es].event_weighted_mean | 1.234830784843807 | 1.386654166134754 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/es].events | 954175 | 224366 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/es].mean_of_session_means | 1.2060700202702723 | 1.3818161996089924 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/es].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/es].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_1s].event_weighted_mean | 0.8486728122217143 | 0.6942142527454042 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_1s].events | 954175 | 224366 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_1s].mean_of_session_means | 0.7947801268883973 | 0.6612899507566828 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_1s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_5s].event_weighted_mean | 0.9376747877548588 | 0.7619673426988904 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_5s].events | 954175 | 224366 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_5s].mean_of_session_means | 0.8824445693363979 | 0.733183027051537 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_5s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_30s].event_weighted_mean | 0.9646011275779165 | 0.8306353557729809 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_30s].events | 954175 | 224366 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_30s].mean_of_session_means | 0.9309166881426323 | 0.7942754850612156 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/mo_30s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_1s].event_weighted_mean | -0.4625148395996217 | -0.001774339356054088 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_1s].events | 954175 | 224366 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_1s].mean_of_session_means | -0.38349023350652206 | 0.059236298095626715 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_1s].sessions_positive | 2 | 2 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_5s].event_weighted_mean | -0.6405187906659106 | -0.1372805192630267 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_5s].events | 954175 | 224366 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_5s].mean_of_session_means | -0.5588191184025231 | -0.08454985449408163 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_5s].sessions_positive | 2 | 1 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_30s].event_weighted_mean | -0.6943714703120266 | -0.2746165454112075 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_30s].events | 954175 | 224366 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_30s].mean_of_session_means | -0.655763356014992 | -0.20673477051343872 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=neutral/rs_30s].sessions_positive | 1 | 1 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/es].event_weighted_mean | 1.5004069754752816 | 1.6177632064691954 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/es].events | 2261364 | 345891 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/es].mean_of_session_means | 1.4647177582594246 | 1.664920263918568 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/es].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/es].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_1s].event_weighted_mean | 1.4295533417728692 | 1.3753453251953527 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_1s].events | 2261364 | 345891 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_1s].mean_of_session_means | 1.3476607816337427 | 1.3312100024104825 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_1s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_5s].event_weighted_mean | 1.6402417202170878 | 1.5652908011323536 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_5s].events | 2261364 | 345891 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_5s].mean_of_session_means | 1.5751359830058036 | 1.5354855480392922 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_5s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_30s].event_weighted_mean | 1.7394356099325707 | 1.6566035598795676 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_30s].events | 2261364 | 345891 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_30s].mean_of_session_means | 1.7102026046652228 | 1.6343377708723712 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/mo_30s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_1s].event_weighted_mean | -1.3586997080704564 | -1.13292744392151 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_1s].events | 2261364 | 345891 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_1s].mean_of_session_means | -1.2306038050080614 | -0.9974997409023972 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_1s].sessions_positive | 0 | 0 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_5s].event_weighted_mean | -1.7800764649588936 | -1.5128183957955121 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_5s].events | 2261364 | 345891 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_5s].mean_of_session_means | -1.6855542077521826 | -1.4060508321600165 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_5s].sessions_positive | 0 | 0 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_30s].event_weighted_mean | -1.9784642443898603 | -1.6954439132899402 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_30s].events | 2261364 | 345891 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_30s].mean_of_session_means | -1.9556874510710212 | -1.6037552778261737 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/touch_imbalance=with/rs_30s].sessions_positive | 0 | 0 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/es].event_weighted_mean | 1.258270514291029 | 1.366865784312895 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/es].events | 3667002 | 673294 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/es].mean_of_session_means | 1.2346653649870496 | 1.3926896985765158 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/es].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/es].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_1s].event_weighted_mean | 0.9529961340853031 | 0.81078067415565 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_1s].events | 3667002 | 673294 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_1s].mean_of_session_means | 0.895516955567531 | 0.7795640432546331 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_1s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_5s].event_weighted_mean | 1.0578344516077631 | 0.9100482484886547 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_5s].events | 3667002 | 673294 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_5s].mean_of_session_means | 1.0019160977227042 | 0.8821408318469833 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_5s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_30s].event_weighted_mean | 1.1069989827273552 | 0.968547088541995 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_30s].events | 3667002 | 673294 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_30s].mean_of_session_means | 1.0709626912820451 | 0.9460455215771567 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/mo_30s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_1s].event_weighted_mean | -0.6477217538795766 | -0.2546955639984048 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_1s].events | 3667002 | 673294 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_1s].mean_of_session_means | -0.5563685461480119 | -0.16643838793275062 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_1s].sessions_positive | 2 | 1 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_5s].event_weighted_mean | -0.8573983889244964 | -0.45323071266441434 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_5s].events | 3667002 | 673294 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_5s].mean_of_session_means | -0.7691668304583587 | -0.37159196511745096 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_5s].sessions_positive | 1 | 1 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_30s].event_weighted_mean | -0.9557274511636804 | -0.5702283927710944 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_30s].events | 3667002 | 673294 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_30s].mean_of_session_means | -0.9072600175770404 | -0.4994013445777976 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=False/rs_30s].sessions_positive | 0 | 1 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/es].event_weighted_mean | 1.6205699922764654 | 1.8140798295633342 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/es].events | 453726 | 46772 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/es].mean_of_session_means | 1.6619146163255614 | 1.92592204884997 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/es].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/es].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_1s].event_weighted_mean | 1.8444308778155845 | 2.006875276361582 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_1s].events | 453726 | 46772 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_1s].mean_of_session_means | 1.8160325111473055 | 2.0375008529651586 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_1s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_5s].event_weighted_mean | 2.0301826188570504 | 2.0605708039181594 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_5s].events | 453726 | 46772 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_5s].mean_of_session_means | 2.009963789829508 | 2.1102539051858584 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_5s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_30s].event_weighted_mean | 2.0544178628032843 | 2.003961008776367 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_30s].events | 453726 | 46772 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_30s].mean_of_session_means | 2.0353601595034 | 1.9778651454957685 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/mo_30s].sessions_positive | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_1s].event_weighted_mean | -2.068291763354704 | -2.1996707231598296 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_1s].events | 453726 | 46772 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_1s].mean_of_session_means | -1.9701504059690493 | -2.149079657080347 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_1s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_1s].sessions_positive | 0 | 0 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_5s].event_weighted_mean | -2.4397952454376344 | -2.307061778272984 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_5s].events | 453726 | 46772 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_5s].mean_of_session_means | -2.358012963333455 | -2.2945857615217475 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_5s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_5s].sessions_positive | 0 | 0 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_30s].event_weighted_mean | -2.4882657333301035 | -2.1938421879893997 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_30s].events | 453726 | 46772 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_30s].mean_of_session_means | -2.408805702681238 | -2.029808242141567 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_30s].sessions | 15 | 5 |
| e001_cells.csv[pre-specified primary (discovery)/primary/qty_ge_touch=True/rs_30s].sessions_positive | 0 | 0 |
| e001_sensitivity.csv[exploratory/unit=trade/all/es].event_weighted_mean | 1.5561295358574403 | 1.8830436326309643 |
| e001_sensitivity.csv[exploratory/unit=trade/all/es].events | 24522089 | 3953664 |
| e001_sensitivity.csv[exploratory/unit=trade/all/es].mean_of_session_means | 1.556675063672903 | 1.8417487185840535 |
| e001_sensitivity.csv[exploratory/unit=trade/all/es].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/unit=trade/all/es].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_1s].event_weighted_mean | 1.6483497931194646 | 1.7476182677623078 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_1s].events | 24522089 | 3953664 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_1s].mean_of_session_means | 1.5949971082695973 | 1.6652090658990641 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_1s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_5s].event_weighted_mean | 1.80619036019763 | 1.8620542301494956 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_5s].events | 24522089 | 3953664 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_5s].mean_of_session_means | 1.7611467169554345 | 1.7962656797141676 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_5s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_30s].event_weighted_mean | 1.8215704723645505 | 1.8584671859190975 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_30s].events | 24522089 | 3953664 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_30s].mean_of_session_means | 1.8013318859554854 | 1.8129996414523817 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/unit=trade/all/mo_30s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_1s].event_weighted_mean | -1.7405700503814892 | -1.6121929028936512 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_1s].events | 24522089 | 3953664 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_1s].mean_of_session_means | -1.6333191528662911 | -1.488669413214075 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_1s].sessions_positive | 0 | 0 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_5s].event_weighted_mean | -2.0562511845378184 | -1.8410648276680266 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_5s].events | 24522089 | 3953664 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_5s].mean_of_session_means | -1.9656183702379655 | -1.7507826408442821 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_5s].sessions_positive | 0 | 0 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_30s].event_weighted_mean | -2.08701140887166 | -1.8338907392072308 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_30s].events | 24522089 | 3953664 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_30s].mean_of_session_means | -2.0459887082380677 | -1.784250564320709 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/unit=trade/all/rs_30s].sessions_positive | 0 | 0 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/es].event_weighted_mean | 1.3192625992694766 | 1.4038261134371561 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/es].events | 4120722 | 720066 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/es].mean_of_session_means | 1.294825749859588 | 1.429167117626658 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/es].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/es].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_1s].event_weighted_mean | 1.061699910613449 | 0.8924275697058617 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_1s].events | 4120722 | 720066 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_1s].mean_of_session_means | 0.9948996309623657 | 0.8534906243013125 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_1s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_5s].event_weighted_mean | 1.1754409636781886 | 0.9887348930859072 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_5s].events | 4120722 | 720066 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_5s].mean_of_session_means | 1.1101560815726343 | 0.9542799497979118 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_5s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_30s].event_weighted_mean | 1.2218540003627276 | 1.0397544096509204 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_30s].events | 4120722 | 720066 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_30s].mean_of_session_means | 1.1766809280617918 | 1.010261599725615 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/mo_30s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_1s].event_weighted_mean | -0.8041372219574212 | -0.38102902597456745 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_1s].events | 4120722 | 720066 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_1s].mean_of_session_means | -0.6949735120651434 | -0.27781413097596674 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_1s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_5s].event_weighted_mean | -1.0316193280869002 | -0.5736436727346581 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_5s].events | 4120722 | 720066 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_5s].mean_of_session_means | -0.9254864132856806 | -0.47939278196916535 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_5s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_30s].event_weighted_mean | -1.1244454014559786 | -0.6756827058646852 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_30s].events | 4120722 | 720066 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_30s].mean_of_session_means | -1.0585361062639953 | -0.5913560818245718 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+0ms/all/rs_30s].sessions_positive | 0 | 1 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/es].event_weighted_mean | 1.4441953599328254 | 1.5314885771480813 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/es].events | 4120688 | 720064 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/es].mean_of_session_means | 1.4097384192090614 | 1.551527595449673 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/es].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/es].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_1s].event_weighted_mean | 1.1241567793294853 | 0.9562577070859387 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_1s].events | 4120688 | 720064 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_1s].mean_of_session_means | 1.0523502635202096 | 0.9146689663513758 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_1s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_5s].event_weighted_mean | 1.237885787550343 | 1.05256535413457 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_5s].events | 4120688 | 720064 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_5s].mean_of_session_means | 1.1675974690294655 | 1.0154590025995796 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_5s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_30s].event_weighted_mean | 1.2842645624309061 | 1.1035741781121327 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_30s].events | 4120688 | 720064 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_30s].mean_of_session_means | 1.2340986091482364 | 1.0714301203306618 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/mo_30s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_1s].event_weighted_mean | -0.8041181987261451 | -0.3810268370237962 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_1s].events | 4120688 | 720064 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_1s].mean_of_session_means | -0.6949621078313574 | -0.2778103372530789 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_1s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_5s].event_weighted_mean | -1.03157621516786 | -0.5736421311210586 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_5s].events | 4120688 | 720064 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_5s].mean_of_session_means | -0.9254565188498692 | -0.4793904097494862 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_5s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_30s].event_weighted_mean | -1.1243337649289868 | -0.6756597790761835 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_30s].events | 4120688 | 720064 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_30s].mean_of_session_means | -1.0584587990874117 | -0.5913326452116506 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+50ms/all/rs_30s].sessions_positive | 0 | 1 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/es].event_weighted_mean | 1.587178635261408 | 1.6337310079265432 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/es].events | 4120561 | 720061 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/es].mean_of_session_means | 1.5360037106623523 | 1.6468052877238377 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/es].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/es].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_1s].event_weighted_mean | 1.1956144135605005 | 1.007383343086837 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_1s].events | 4120561 | 720061 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_1s].mean_of_session_means | 1.1154598513274931 | 0.9623107482593596 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_1s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_5s].event_weighted_mean | 1.3093143358293042 | 1.1036958756657946 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_5s].events | 4120561 | 720061 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_5s].mean_of_session_means | 1.2306819782855305 | 1.0631061673221107 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_5s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_30s].event_weighted_mean | 1.3555277922460338 | 1.1546914846658713 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_30s].events | 4120561 | 720061 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_30s].mean_of_session_means | 1.297063415118091 | 1.1190629900156925 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/mo_30s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_1s].event_weighted_mean | -0.8040501918595929 | -0.38103567824713125 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_1s].events | 4120561 | 720061 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_1s].mean_of_session_means | -0.6949159919926337 | -0.2778162087948817 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_1s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_5s].event_weighted_mean | -1.0314500363972003 | -0.5736607434050458 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_5s].events | 4120561 | 720061 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_5s].mean_of_session_means | -0.9253602459087086 | -0.4794070469203839 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_5s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_30s].event_weighted_mean | -1.1238769492306593 | -0.6756519614051996 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_30s].events | 4120561 | 720061 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_30s].mean_of_session_means | -1.0581231195738305 | -0.5913206923075475 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/timing=receipt+200ms/all/rs_30s].sessions_positive | 0 | 1 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/es].event_weighted_mean | 1.3151312614967403 | 1.3959146427848321 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/es].events | 3888361 | 720066 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/es].mean_of_session_means | 1.294364718848737 | 1.421297260156206 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/es].sessions | 14 | 5 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/es].sessions_positive | 14 | 5 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_1s].event_weighted_mean | 1.0522891630443476 | 0.8884731866953005 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_1s].events | 3888361 | 720066 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_1s].mean_of_session_means | 0.9819909533277243 | 0.8495563617275075 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_1s].sessions | 14 | 5 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_1s].sessions_positive | 14 | 5 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_5s].event_weighted_mean | 1.1672130035081814 | 0.9847806215802167 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_5s].events | 3888361 | 720066 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_5s].mean_of_session_means | 1.0987693629470432 | 0.950346001959705 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_5s].sessions | 14 | 5 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_5s].sessions_positive | 14 | 5 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_30s].event_weighted_mean | 1.2143601300162856 | 1.035802562175248 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_30s].events | 3888361 | 720066 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_30s].mean_of_session_means | 1.1676081100669464 | 1.006330049731746 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_30s].sessions | 14 | 5 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/mo_30s].sessions_positive | 14 | 5 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_1s].event_weighted_mean | -0.7894470645919549 | -0.38103173060576884 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_1s].events | 3888361 | 720066 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_1s].mean_of_session_means | -0.6696171878067115 | -0.2778154632988091 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_1s].sessions | 14 | 5 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_1s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_5s].event_weighted_mean | -1.0192947455196224 | -0.5736466003756019 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_5s].events | 3888361 | 720066 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_5s].mean_of_session_means | -0.9031740070453491 | -0.4793947437632041 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_5s].sessions | 14 | 5 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_5s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_30s].event_weighted_mean | -1.1135889985358303 | -0.6756904815656638 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_30s].events | 3888361 | 720066 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_30s].mean_of_session_means | -1.0408515012851562 | -0.5913628393072864 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_30s].sessions | 14 | 5 |
| e001_sensitivity.csv[exploratory/eligible_sessions_only(posthoc)/all/rs_30s].sessions_positive | 0 | 1 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/es].event_weighted_mean | 1.2981626627047125 | 1.3959152337856549 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/es].events | 4120728 | 720065 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/es].mean_of_session_means | 1.2756880791802852 | 1.4212977047384336 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/es].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/es].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_1s].event_weighted_mean | 1.0511504215155254 | 0.8884730729799433 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_1s].events | 4120728 | 720065 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_1s].mean_of_session_means | 0.9853312268303135 | 0.8495562005973276 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_1s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_5s].event_weighted_mean | 1.1648979715812606 | 0.9847806416131114 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_5s].events | 4120728 | 720065 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_5s].mean_of_session_means | 1.100595332654191 | 0.9503459710426865 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_5s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_30s].event_weighted_mean | 1.2113175834166825 | 1.0357986102820451 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_30s].events | 4120728 | 720065 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_30s].mean_of_session_means | 1.167127869658535 | 1.0063263056230156 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/mo_30s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_1s].event_weighted_mean | -0.8041381803263382 | -0.38103091217423174 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_1s].events | 4120728 | 720065 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_1s].mean_of_session_means | -0.6949743744803417 | -0.2778146964562219 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_1s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_5s].event_weighted_mean | -1.0316332804578083 | -0.5736460494405684 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_5s].events | 4120728 | 720065 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_5s].mean_of_session_means | -0.925502586128097 | -0.47939423734693926 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_5s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_30s].event_weighted_mean | -1.1244725041286525 | -0.675681986778435 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_30s].events | 4120728 | 720065 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_30s].mean_of_session_means | -1.0585676601367848 | -0.5913549065075975 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=0.5/all/rs_30s].sessions_positive | 0 | 1 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/es].event_weighted_mean | 1.2981623360648884 | 1.3959144143847284 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/es].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/es].mean_of_session_means | 1.2756878860552174 | 1.421296875168103 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/es].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/es].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_1s].event_weighted_mean | 1.0511510637098722 | 0.8884719528195824 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_1s].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_1s].mean_of_session_means | 0.9853316775353727 | 0.8495550756573224 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_1s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_5s].event_weighted_mean | 1.1648971630291225 | 0.9847792539566185 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_5s].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_5s].mean_of_session_means | 1.1005948383790354 | 0.9503444475274077 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_5s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_30s].event_weighted_mean | 1.2113137245117513 | 1.035797703314763 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_30s].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_30s].mean_of_session_means | 1.167125014436961 | 1.0063246056151685 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/mo_30s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_1s].event_weighted_mean | -0.8041397913548559 | -0.3810294912544363 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_1s].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_1s].mean_of_session_means | -0.6949754690155276 | -0.2778132761465411 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_1s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_5s].event_weighted_mean | -1.0316319899933561 | -0.573644093528509 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_5s].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_5s].mean_of_session_means | -0.9255017907028531 | -0.4793920198867121 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_5s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_30s].event_weighted_mean | -1.1244651129586145 | -0.6756809922447977 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_30s].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_30s].mean_of_session_means | -1.0585621428187046 | -0.5913523360622337 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=2/all/rs_30s].sessions_positive | 0 | 1 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/es].event_weighted_mean | 1.2981623360648884 | 1.3959144143847284 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/es].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/es].mean_of_session_means | 1.2756878860552174 | 1.421296875168103 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/es].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/es].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_1s].event_weighted_mean | 1.0511510637098722 | 0.8884719528195824 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_1s].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_1s].mean_of_session_means | 0.9853316775353727 | 0.8495550756573224 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_1s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_5s].event_weighted_mean | 1.1648971630291225 | 0.9847792539566185 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_5s].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_5s].mean_of_session_means | 1.1005948383790354 | 0.9503444475274077 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_5s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_30s].event_weighted_mean | 1.2113137245117513 | 1.035797703314763 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_30s].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_30s].mean_of_session_means | 1.167125014436961 | 1.0063246056151685 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/mo_30s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_1s].event_weighted_mean | -0.8041397913548559 | -0.3810294912544363 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_1s].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_1s].mean_of_session_means | -0.6949754690155276 | -0.2778132761465411 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_1s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_5s].event_weighted_mean | -1.0316319899933561 | -0.573644093528509 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_5s].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_5s].mean_of_session_means | -0.9255017907028531 | -0.4793920198867121 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_5s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_30s].event_weighted_mean | -1.1244651129586145 | -0.6756809922447977 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_30s].events | 4120730 | 720067 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_30s].mean_of_session_means | -1.0585621428187046 | -0.5913523360622337 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:silence_s=5/all/rs_30s].sessions_positive | 0 | 1 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/es].event_weighted_mean | 1.3028723394256023 | 1.3959146427848321 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/es].events | 4023446 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/es].mean_of_session_means | 1.2780243535837112 | 1.421297260156206 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/es].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/es].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_1s].event_weighted_mean | 1.0513402115279036 | 0.8884731866953005 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_1s].events | 4023446 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_1s].mean_of_session_means | 0.9886291753584574 | 0.8495563617275075 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_1s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_5s].event_weighted_mean | 1.164944671895679 | 0.9847806215802167 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_5s].events | 4023446 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_5s].mean_of_session_means | 1.103516110145997 | 0.950346001959705 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_5s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_30s].event_weighted_mean | 1.2026984032440295 | 1.035802562175248 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_30s].events | 4023446 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_30s].mean_of_session_means | 1.16222027052154 | 1.006330049731746 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/mo_30s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_1s].event_weighted_mean | -0.7998080836302045 | -0.38103173060576884 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_1s].events | 4023446 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_1s].mean_of_session_means | -0.6992339971332032 | -0.2778154632988091 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_1s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_5s].event_weighted_mean | -1.0270170043657556 | -0.5736466003756019 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_5s].events | 4023446 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_5s].mean_of_session_means | -0.9290078667082826 | -0.4793947437632041 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_5s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_30s].event_weighted_mean | -1.1025244670624568 | -0.6756904815656638 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_30s].events | 4023446 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_30s].mean_of_session_means | -1.0464161874593692 | -0.5913628393072864 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=800/all/rs_30s].sessions_positive | 0 | 1 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/es].event_weighted_mean | 1.315580705079831 | 1.3959146427848321 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/es].events | 3684122 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/es].mean_of_session_means | 1.2851298956818258 | 1.421297260156206 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/es].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/es].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_1s].event_weighted_mean | 1.0536302454301267 | 0.8884731866953005 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_1s].events | 3684122 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_1s].mean_of_session_means | 1.001952603979165 | 0.8495563617275075 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_1s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_5s].event_weighted_mean | 1.1698985359673855 | 0.9847806215802167 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_5s].events | 3684122 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_5s].mean_of_session_means | 1.1180224369548748 | 0.950346001959705 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_5s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_30s].event_weighted_mean | 1.2088243131895549 | 1.035802562175248 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_30s].events | 3684122 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_30s].mean_of_session_means | 1.1721431713634465 | 1.006330049731746 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/mo_30s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_1s].event_weighted_mean | -0.7916797857804222 | -0.38103173060576884 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_1s].events | 3684122 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_1s].mean_of_session_means | -0.7187753122765043 | -0.2778154632988091 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_1s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_5s].event_weighted_mean | -1.0242163668549398 | -0.5736466003756019 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_5s].events | 3684122 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_5s].mean_of_session_means | -0.9509149782279234 | -0.4793947437632041 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_5s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_30s].event_weighted_mean | -1.1020679212992786 | -0.6756904815656638 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_30s].events | 3684122 | 720066 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_30s].mean_of_session_means | -1.0591564470450676 | -0.5913628393072864 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=600/all/rs_30s].sessions_positive | 0 | 1 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/es].event_weighted_mean | 1.3185854363455831 | 1.384437883828743 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/es].events | 3039729 | 687006 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/es].mean_of_session_means | 1.2731321216550617 | 1.4168691567417702 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/es].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/es].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_1s].event_weighted_mean | 1.0258982182653653 | 0.8700128986257193 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_1s].events | 3039729 | 687006 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_1s].mean_of_session_means | 0.9840718176429749 | 0.8443336459496364 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_1s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_5s].event_weighted_mean | 1.147629540672902 | 0.9655018851098164 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_5s].events | 3039729 | 687006 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_5s].mean_of_session_means | 1.104679956249392 | 0.9423372528023812 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_5s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_30s].event_weighted_mean | 1.172866697119845 | 1.0282147626865406 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_30s].events | 3039729 | 687006 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_30s].mean_of_session_means | 1.1471374241548462 | 1.0076868966375954 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/mo_30s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_1s].event_weighted_mean | -0.733211000185148 | -0.35558791342269586 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_1s].events | 3039729 | 687006 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_1s].mean_of_session_means | -0.6950115136308885 | -0.2717981351575032 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_1s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_5s].event_weighted_mean | -0.976673645000221 | -0.54656588639089 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_5s].events | 3039729 | 687006 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_5s].mean_of_session_means | -0.9362277908437224 | -0.46780534886299235 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_5s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_30s].event_weighted_mean | -1.0271479578941076 | -0.6719916415443381 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_30s].events | 3039729 | 687006 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_30s].mean_of_session_means | -1.0211427266546311 | -0.5985046365334206 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/windows:proven_levels=400/all/rs_30s].sessions_positive | 0 | 1 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/es].event_weighted_mean | 1.2969570208616332 | 1.3955492573621977 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/es].events | 4134484 | 720889 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/es].mean_of_session_means | 1.2754229125404826 | 1.4208159859549054 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/es].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/es].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_1s].event_weighted_mean | 1.0506330382272062 | 0.8879098820888102 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_1s].events | 4133439 | 720853 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_1s].mean_of_session_means | 0.9845940692537591 | 0.8490023285557824 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_1s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_5s].event_weighted_mean | 1.1644689463938334 | 0.9842847648397225 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_5s].events | 4130965 | 720729 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_5s].mean_of_session_means | 1.100348221265564 | 0.9497968623871037 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_5s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_30s].event_weighted_mean | 1.2113175834166825 | 1.035802562175248 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_30s].events | 4120728 | 720066 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_30s].mean_of_session_means | 1.167127869658535 | 1.006330049731746 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/mo_30s].sessions_positive | 15 | 5 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_1s].event_weighted_mean | -0.8044905150401513 | -0.38015038296017317 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_1s].events | 4133439 | 720853 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_1s].mean_of_session_means | -0.6940364735634634 | -0.27705217579446934 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_1s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_1s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_5s].event_weighted_mean | -1.031764189746712 | -0.5728821292846532 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_5s].events | 4130965 | 720729 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_5s].mean_of_session_means | -0.9253019987209711 | -0.47860617172392284 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_5s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_5s].sessions_positive | 1 | 1 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_30s].event_weighted_mean | -1.1244725041286525 | -0.6756904815656638 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_30s].events | 4120728 | 720066 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_30s].mean_of_session_means | -1.0585676601367848 | -0.5913628393072864 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_30s].sessions | 15 | 5 |
| e001_sensitivity.csv[exploratory/available_case_per_horizon/all/rs_30s].sessions_positive | 0 | 1 |
| exclusions.eligible_sessions_only(posthoc).horizon_beyond_session_data | 562 | 199 |
| exclusions.eligible_sessions_only(posthoc).horizon_leaves_window | 6324 | 624 |
| exclusions.eligible_sessions_only(posthoc).included | 3888361 | 720066 |
| exclusions.eligible_sessions_only(posthoc).t_outside_windows | 62785 | 256 |
| exclusions.primary.horizon_beyond_session_data | 562 | 199 |
| exclusions.primary.horizon_leaves_window | 13194 | 624 |
| exclusions.primary.included | 4120728 | 720066 |
| exclusions.primary.t_outside_windows | 176450 | 256 |
| exclusions.timing=receipt+0ms.horizon_beyond_session_data | 562 | 199 |
| exclusions.timing=receipt+0ms.horizon_leaves_window | 13187 | 624 |
| exclusions.timing=receipt+0ms.included | 4120722 | 720066 |
| exclusions.timing=receipt+0ms.t_outside_windows | 176450 | 256 |
| exclusions.timing=receipt+200ms.horizon_beyond_session_data | 562 | 199 |
| exclusions.timing=receipt+200ms.horizon_leaves_window | 13026 | 624 |
| exclusions.timing=receipt+200ms.included | 4120561 | 720061 |
| exclusions.timing=receipt+200ms.no_pre_state | 19 | 2 |
| exclusions.timing=receipt+200ms.pre_state_in_other_window | 13 | 3 |
| exclusions.timing=receipt+200ms.t_outside_windows | 176450 | 256 |
| exclusions.timing=receipt+50ms.horizon_beyond_session_data | 562 | 199 |
| exclusions.timing=receipt+50ms.horizon_leaves_window | 13126 | 624 |
| exclusions.timing=receipt+50ms.included | 4120688 | 720064 |
| exclusions.timing=receipt+50ms.no_pre_state | 1 | 1 |
| exclusions.timing=receipt+50ms.pre_state_outside_windows | 6 | 1 |
| exclusions.timing=receipt+50ms.t_outside_windows | 176450 | 256 |
| exclusions.unit=trade.horizon_beyond_session_data | 3124 | 887 |
| exclusions.unit=trade.horizon_leaves_window | 76639 | 3771 |
| exclusions.unit=trade.included | 24522089 | 3953664 |
| exclusions.unit=trade.t_outside_windows | 1087421 | 717 |
| exclusions.windows:proven_levels=400.horizon_beyond_session_data | 455 | 199 |
| exclusions.windows:proven_levels=400.horizon_leaves_window | 38382 | 3365 |
| exclusions.windows:proven_levels=400.included | 3039729 | 687006 |
| exclusions.windows:proven_levels=400.t_outside_windows | 1232368 | 30575 |
| exclusions.windows:proven_levels=600.horizon_beyond_session_data | 562 | 199 |
| exclusions.windows:proven_levels=600.horizon_leaves_window | 17413 | 624 |
| exclusions.windows:proven_levels=600.included | 3684122 | 720066 |
| exclusions.windows:proven_levels=600.t_outside_windows | 608836 | 256 |
| exclusions.windows:proven_levels=800.horizon_beyond_session_data | 562 | 199 |
| exclusions.windows:proven_levels=800.horizon_leaves_window | 8725 | 624 |
| exclusions.windows:proven_levels=800.included | 4023446 | 720066 |
| exclusions.windows:proven_levels=800.t_outside_windows | 278201 | 256 |
| exclusions.windows:silence_s=0.5.horizon_beyond_session_data | 562 | 199 |
| exclusions.windows:silence_s=0.5.horizon_leaves_window | 13194 | 624 |
| exclusions.windows:silence_s=0.5.included | 4120728 | 720065 |
| exclusions.windows:silence_s=0.5.t_outside_windows | 176450 | 257 |
| exclusions.windows:silence_s=2.horizon_beyond_session_data | 562 | 199 |
| exclusions.windows:silence_s=2.horizon_leaves_window | 13194 | 624 |
| exclusions.windows:silence_s=2.included | 4120730 | 720067 |
| exclusions.windows:silence_s=2.t_outside_windows | 176448 | 255 |
| exclusions.windows:silence_s=5.horizon_beyond_session_data | 562 | 199 |
| exclusions.windows:silence_s=5.horizon_leaves_window | 13194 | 624 |
| exclusions.windows:silence_s=5.included | 4120730 | 720067 |
| exclusions.windows:silence_s=5.t_outside_windows | 176448 | 255 |
| proxy_validation_qty_ge_touch[0].events | 3667002 | 673294 |
| proxy_validation_qty_ge_touch[0].qty_ge_touch | False | False |
| proxy_validation_qty_ge_touch[0].share_touch_moved_next_state | 0.39136220814714584 | 0.3531176573681037 |
| proxy_validation_qty_ge_touch[1].events | 453726 | 46772 |
| proxy_validation_qty_ge_touch[1].qty_ge_touch | True | True |
| proxy_validation_qty_ge_touch[1].share_touch_moved_next_state | 0.933384906309094 | 0.9405627298383649 |
| sensitivity_specs[exploratory/unit=trade].factor_changed |  | event unit |
| sensitivity_specs[exploratory/timing=receipt+0ms].factor_changed |  | information clock |
| sensitivity_specs[exploratory/timing=receipt+50ms].factor_changed |  | information clock |
| sensitivity_specs[exploratory/timing=receipt+200ms].factor_changed |  | information clock |
| sensitivity_specs[exploratory/eligible_sessions_only(posthoc)].factor_changed |  | session set |
| sensitivity_specs[exploratory/windows:silence_s=0.5].factor_changed |  | validity windows |
| sensitivity_specs[exploratory/windows:silence_s=2].factor_changed |  | validity windows |
| sensitivity_specs[exploratory/windows:silence_s=5].factor_changed |  | validity windows |
| sensitivity_specs[exploratory/windows:proven_levels=800].factor_changed |  | validity windows |
| sensitivity_specs[exploratory/windows:proven_levels=600].factor_changed |  | validity windows |
| sensitivity_specs[exploratory/windows:proven_levels=400].factor_changed |  | validity windows |
| sensitivity_specs[exploratory/available_case_per_horizon].factor_changed |  | event set per horizon |

Not computed on test: exploratory tables (exploratory by declaration (protocol section 11)).

## E002

State: complete. Status: modeled historical replay; VIP0 attainable; other schedules hypothetical.

E002 §10.10: the test sessions only report the same tables; no confirmation claim is made.

| Item (reported only) | Discovery | Test |
|---|---|---|
| descriptive_range_of_means[P0/distant].range_bp_across_fill_models | 0.531154906213855 | 0.6471878012176493 |
| descriptive_range_of_means[P0/regional].range_bp_across_fill_models | 0.4893774853059334 | 0.6223343223724829 |
| descriptive_range_of_means[P0/tokyo].range_bp_across_fill_models | 0.49133987707167215 | 0.6720609756637863 |
| descriptive_range_of_means[P1/distant].range_bp_across_fill_models | 0.5502331067681876 | 0.6714613277789638 |
| descriptive_range_of_means[P1/regional].range_bp_across_fill_models | 0.5054290539121631 | 0.6085215416874998 |
| descriptive_range_of_means[P1/tokyo].range_bp_across_fill_models | 0.4900384110046492 | 0.589701173439531 |
| model_pair_t_intervals_95_descriptive_not_used[P0/distant/intermediate - conservative].t_interval |  | [0.049901340952252654, 0.34121128775280307] |
| model_pair_t_intervals_95_descriptive_not_used[P0/distant/optimistic - conservative].t_interval |  | [0.4434678184816795, 0.8509077839536213] |
| model_pair_t_intervals_95_descriptive_not_used[P0/distant/optimistic - intermediate].t_interval |  | [0.2919050493002023, 0.6113579244300427] |
| model_pair_t_intervals_95_descriptive_not_used[P0/regional/intermediate - conservative].t_interval |  | [0.05408589048197243, 0.3961809141811199] |
| model_pair_t_intervals_95_descriptive_not_used[P0/regional/optimistic - conservative].t_interval |  | [0.4218247605652498, 0.8228438841797201] |
| model_pair_t_intervals_95_descriptive_not_used[P0/regional/optimistic - intermediate].t_interval |  | [0.2875830504789491, 0.5068187896029286] |
| model_pair_t_intervals_95_descriptive_not_used[P0/tokyo/intermediate - conservative].t_interval |  | [0.07517399796785301, 0.5073860935310517] |
| model_pair_t_intervals_95_descriptive_not_used[P0/tokyo/optimistic - conservative].t_interval |  | [0.2932400905017002, 1.0508818608258723] |
| model_pair_t_intervals_95_descriptive_not_used[P0/tokyo/optimistic - intermediate].t_interval |  | [0.21287836671961033, 0.5486834931090576] |
| model_pair_t_intervals_95_descriptive_not_used[P1/distant/intermediate - conservative].t_interval |  | [0.17477865118064556, 0.31557039574062784] |
| model_pair_t_intervals_95_descriptive_not_used[P1/distant/optimistic - conservative].t_interval |  | [0.49076914040986475, 0.8521535151480643] |
| model_pair_t_intervals_95_descriptive_not_used[P1/distant/optimistic - intermediate].t_interval |  | [0.3100862143398171, 0.5424873942968386] |
| model_pair_t_intervals_95_descriptive_not_used[P1/regional/intermediate - conservative].t_interval |  | [0.177696396234167, 0.33185001726190655] |
| model_pair_t_intervals_95_descriptive_not_used[P1/regional/optimistic - conservative].t_interval |  | [0.44308044319155104, 0.7739626401834486] |
| model_pair_t_intervals_95_descriptive_not_used[P1/regional/optimistic - intermediate].t_interval |  | [0.25768298552062024, 0.4498136843583059] |
| model_pair_t_intervals_95_descriptive_not_used[P1/tokyo/intermediate - conservative].t_interval |  | [0.18167909768158808, 0.34480773304551493] |
| model_pair_t_intervals_95_descriptive_not_used[P1/tokyo/optimistic - conservative].t_interval |  | [0.4199685893947296, 0.7594337574843295] |
| model_pair_t_intervals_95_descriptive_not_used[P1/tokyo/optimistic - intermediate].t_interval |  | [0.2197709972852837, 0.4331445188666725] |
| model_pairs_table[P0/distant/intermediate - conservative].mean | 0.18368421482971692 | 0.19555631435252785 |
| model_pairs_table[P0/distant/intermediate - conservative].sessions_defined | 15 | 5 |
| model_pairs_table[P0/distant/optimistic - conservative].mean | 0.5311549062138538 | 0.6471878012176504 |
| model_pairs_table[P0/distant/optimistic - conservative].sessions_defined | 15 | 5 |
| model_pairs_table[P0/distant/optimistic - intermediate].mean | 0.3474706913841369 | 0.4516314868651225 |
| model_pairs_table[P0/distant/optimistic - intermediate].sessions_defined | 15 | 5 |
| model_pairs_table[P0/regional/intermediate - conservative].mean | 0.16074284424430635 | 0.22513340233154616 |
| model_pairs_table[P0/regional/intermediate - conservative].sessions_defined | 15 | 5 |
| model_pairs_table[P0/regional/optimistic - conservative].mean | 0.4893774853059339 | 0.622334322372485 |
| model_pairs_table[P0/regional/optimistic - conservative].sessions_defined | 15 | 5 |
| model_pairs_table[P0/regional/optimistic - intermediate].mean | 0.32863464106162754 | 0.3972009200409389 |
| model_pairs_table[P0/regional/optimistic - intermediate].sessions_defined | 15 | 5 |
| model_pairs_table[P0/tokyo/intermediate - conservative].mean | 0.17551077759790806 | 0.2912800457494523 |
| model_pairs_table[P0/tokyo/intermediate - conservative].sessions_defined | 15 | 5 |
| model_pairs_table[P0/tokyo/optimistic - conservative].mean | 0.491339877071671 | 0.6720609756637863 |
| model_pairs_table[P0/tokyo/optimistic - conservative].sessions_defined | 15 | 5 |
| model_pairs_table[P0/tokyo/optimistic - intermediate].mean | 0.31582909947376286 | 0.380780929914334 |
| model_pairs_table[P0/tokyo/optimistic - intermediate].sessions_defined | 15 | 5 |
| model_pairs_table[P1/distant/intermediate - conservative].mean | 0.19599087166018733 | 0.2451745234606367 |
| model_pairs_table[P1/distant/intermediate - conservative].sessions_defined | 15 | 5 |
| model_pairs_table[P1/distant/optimistic - conservative].mean | 0.5502331067681862 | 0.6714613277789645 |
| model_pairs_table[P1/distant/optimistic - conservative].sessions_defined | 15 | 5 |
| model_pairs_table[P1/distant/optimistic - intermediate].mean | 0.35424223510799885 | 0.4262868043183278 |
| model_pairs_table[P1/distant/optimistic - intermediate].sessions_defined | 15 | 5 |
| model_pairs_table[P1/regional/intermediate - conservative].mean | 0.183445405340757 | 0.2547732067480368 |
| model_pairs_table[P1/regional/intermediate - conservative].sessions_defined | 15 | 5 |
| model_pairs_table[P1/regional/optimistic - conservative].mean | 0.5054290539121669 | 0.6085215416874998 |
| model_pairs_table[P1/regional/optimistic - conservative].sessions_defined | 15 | 5 |
| model_pairs_table[P1/regional/optimistic - intermediate].mean | 0.3219836485714099 | 0.35374833493946306 |
| model_pairs_table[P1/regional/optimistic - intermediate].sessions_defined | 15 | 5 |
| model_pairs_table[P1/tokyo/intermediate - conservative].mean | 0.187594155207515 | 0.2632434153635515 |
| model_pairs_table[P1/tokyo/intermediate - conservative].sessions_defined | 15 | 5 |
| model_pairs_table[P1/tokyo/optimistic - conservative].mean | 0.4900384110046519 | 0.5897011734395295 |
| model_pairs_table[P1/tokyo/optimistic - conservative].sessions_defined | 15 | 5 |
| model_pairs_table[P1/tokyo/optimistic - intermediate].mean | 0.3024442557971369 | 0.3264577580759781 |
| model_pairs_table[P1/tokyo/optimistic - intermediate].sessions_defined | 15 | 5 |
| paired_t_intervals_95_descriptive_not_used[conservative/distant].t_interval |  | [-0.17476810447207658, 0.09867771675376831] |
| paired_t_intervals_95_descriptive_not_used[conservative/regional].t_interval |  | [-0.13717309165750044, 0.14845701037228812] |
| paired_t_intervals_95_descriptive_not_used[conservative/tokyo].t_interval |  | [-0.1366613768981315, 0.37035852992377916] |
| paired_t_intervals_95_descriptive_not_used[intermediate/distant].t_interval |  | [-0.10344618919422435, 0.12659221969213383] |
| paired_t_intervals_95_descriptive_not_used[intermediate/regional].t_interval |  | [-0.019950543026767374, 0.09051407057453634] |
| paired_t_intervals_95_descriptive_not_used[intermediate/tokyo].t_interval |  | [-0.027934836742815605, 0.2055587289966617] |
| paired_t_intervals_95_descriptive_not_used[optimistic/distant].t_interval |  | [-0.07787332723071923, 0.05032999263503935] |
| paired_t_intervals_95_descriptive_not_used[optimistic/regional].t_interval |  | [-0.050835018592861714, 0.03449337593767905] |
| paired_t_intervals_95_descriptive_not_used[optimistic/tokyo].t_interval |  | [-0.0037429661050042487, 0.07272051468213847] |
| paired_table[conservative/distant].mean_p1_minus_p0 | 0.008642249469145113 | -0.03804519385915413 |
| paired_table[conservative/distant].sessions | 15 | 5 |
| paired_table[conservative/distant].sessions_defined | 15 | 5 |
| paired_table[conservative/regional].mean_p1_minus_p0 | 0.008418474326620165 | 0.005641959357393844 |
| paired_table[conservative/regional].sessions | 15 | 5 |
| paired_table[conservative/regional].sessions_defined | 15 | 5 |
| paired_table[conservative/tokyo].mean_p1_minus_p0 | 0.07166395036848563 | 0.11684857651282385 |
| paired_table[conservative/tokyo].sessions | 15 | 5 |
| paired_table[conservative/tokyo].sessions_defined | 15 | 5 |
| paired_table[intermediate/distant].mean_p1_minus_p0 | 0.020948906299615544 | 0.011573015248954733 |
| paired_table[intermediate/distant].sessions | 15 | 5 |
| paired_table[intermediate/distant].sessions_defined | 15 | 5 |
| paired_table[intermediate/regional].mean_p1_minus_p0 | 0.031121035423070844 | 0.03528176377388448 |
| paired_table[intermediate/regional].sessions | 15 | 5 |
| paired_table[intermediate/regional].sessions_defined | 15 | 5 |
| paired_table[intermediate/tokyo].mean_p1_minus_p0 | 0.08374732797809253 | 0.08881194612692304 |
| paired_table[intermediate/tokyo].sessions | 15 | 5 |
| paired_table[intermediate/tokyo].sessions_defined | 15 | 5 |
| paired_table[optimistic/distant].mean_p1_minus_p0 | 0.027720450023477502 | -0.01377166729783994 |
| paired_table[optimistic/distant].sessions | 15 | 5 |
| paired_table[optimistic/distant].sessions_defined | 15 | 5 |
| paired_table[optimistic/regional].mean_p1_minus_p0 | 0.024470042932853174 | -0.008170821327591327 |
| paired_table[optimistic/regional].sessions | 15 | 5 |
| paired_table[optimistic/regional].sessions_defined | 15 | 5 |
| paired_table[optimistic/tokyo].mean_p1_minus_p0 | 0.07036248430146656 | 0.034488774288567114 |
| paired_table[optimistic/tokyo].sessions | 15 | 5 |
| paired_table[optimistic/tokyo].sessions_defined | 15 | 5 |
| scenario_t_intervals_95_descriptive_not_used[P0/conservative/distant].t_interval |  | [-11.958546076649412, -11.315373175420966] |
| scenario_t_intervals_95_descriptive_not_used[P0/conservative/regional].t_interval |  | [-11.995518662225802, -11.40567434961595] |
| scenario_t_intervals_95_descriptive_not_used[P0/conservative/tokyo].t_interval |  | [-12.403483499580757, -11.491231129910796] |
| scenario_t_intervals_95_descriptive_not_used[P0/intermediate/distant].t_interval |  | [-11.670923006578263, -11.211883616787059] |
| scenario_t_intervals_95_descriptive_not_used[P0/intermediate/regional].t_interval |  | [-11.633028880495955, -11.317897326682706] |
| scenario_t_intervals_95_descriptive_not_used[P0/intermediate/tokyo].t_interval |  | [-11.90935893016437, -11.402795607828278] |
| scenario_t_intervals_95_descriptive_not_used[P0/optimistic/distant].t_interval |  | [-11.125304294445614, -10.854239355189465] |
| scenario_t_intervals_95_descriptive_not_used[P0/optimistic/regional].t_interval |  | [-11.19054612648885, -10.965978240607935] |
| scenario_t_intervals_95_descriptive_not_used[P0/optimistic/tokyo].t_interval |  | [-11.394177644764122, -11.156415033399858] |
| scenario_t_intervals_95_descriptive_not_used[P1/conservative/distant].t_interval |  | [-11.876666358816175, -11.473343280972513] |
| scenario_t_intervals_95_descriptive_not_used[P1/conservative/regional].t_interval |  | [-11.875777222747905, -11.514131870379062] |
| scenario_t_intervals_95_descriptive_not_used[P1/conservative/tokyo].t_interval |  | [-12.054886306203112, -11.606131170262795] |
| scenario_t_intervals_95_descriptive_not_used[P1/intermediate/distant].t_interval |  | [-11.578825825427664, -11.28083476743975] |
| scenario_t_intervals_95_descriptive_not_used[P1/intermediate/regional].t_interval |  | [-11.573553766255243, -11.306808913375653] |
| scenario_t_intervals_95_descriptive_not_used[P1/intermediate/tokyo].t_interval |  | [-11.72170733145326, -11.412823314285546] |
| scenario_t_intervals_95_descriptive_not_used[P1/optimistic/distant].t_interval |  | [-11.156897480759255, -10.850189503471505] |
| scenario_t_intervals_95_descriptive_not_used[P1/optimistic/regional].t_interval |  | [-11.203042030870641, -10.969823978881326] |
| scenario_t_intervals_95_descriptive_not_used[P1/optimistic/tokyo].t_interval |  | [-11.357393217155481, -11.124221912431365] |
| scenario_table[P0/conservative/distant].mean | -11.62861257586416 | -11.636959626035189 |
| scenario_table[P0/conservative/distant].sessions | 15 | 5 |
| scenario_table[P0/conservative/distant].sessions_defined | 15 | 5 |
| scenario_table[P0/conservative/regional].mean | -11.653145683803832 | -11.700596505920876 |
| scenario_table[P0/conservative/regional].sessions | 15 | 5 |
| scenario_table[P0/conservative/regional].sessions_defined | 15 | 5 |
| scenario_table[P0/conservative/tokyo].mean | -11.865107069286603 | -11.947357314745776 |
| scenario_table[P0/conservative/tokyo].sessions | 15 | 5 |
| scenario_table[P0/conservative/tokyo].sessions_defined | 15 | 5 |
| scenario_table[P0/intermediate/distant].mean | -11.44492836103444 | -11.441403311682661 |
| scenario_table[P0/intermediate/distant].sessions | 15 | 5 |
| scenario_table[P0/intermediate/distant].sessions_defined | 15 | 5 |
| scenario_table[P0/intermediate/regional].mean | -11.492402839559528 | -11.47546310358933 |
| scenario_table[P0/intermediate/regional].sessions | 15 | 5 |
| scenario_table[P0/intermediate/regional].sessions_defined | 15 | 5 |
| scenario_table[P0/intermediate/tokyo].mean | -11.689596291688696 | -11.656077268996324 |
| scenario_table[P0/intermediate/tokyo].sessions | 15 | 5 |
| scenario_table[P0/intermediate/tokyo].sessions_defined | 15 | 5 |
| scenario_table[P0/optimistic/distant].mean | -11.097457669650305 | -10.98977182481754 |
| scenario_table[P0/optimistic/distant].sessions | 15 | 5 |
| scenario_table[P0/optimistic/distant].sessions_defined | 15 | 5 |
| scenario_table[P0/optimistic/regional].mean | -11.163768198497898 | -11.078262183548393 |
| scenario_table[P0/optimistic/regional].sessions | 15 | 5 |
| scenario_table[P0/optimistic/regional].sessions_defined | 15 | 5 |
| scenario_table[P0/optimistic/tokyo].mean | -11.373767192214931 | -11.27529633908199 |
| scenario_table[P0/optimistic/tokyo].sessions | 15 | 5 |
| scenario_table[P0/optimistic/tokyo].sessions_defined | 15 | 5 |
| scenario_table[P1/conservative/distant].mean | -11.619970326395014 | -11.675004819894344 |
| scenario_table[P1/conservative/distant].sessions | 15 | 5 |
| scenario_table[P1/conservative/distant].sessions_defined | 15 | 5 |
| scenario_table[P1/conservative/regional].mean | -11.644727209477209 | -11.694954546563483 |
| scenario_table[P1/conservative/regional].sessions | 15 | 5 |
| scenario_table[P1/conservative/regional].sessions_defined | 15 | 5 |
| scenario_table[P1/conservative/tokyo].mean | -11.793443118918116 | -11.830508738232954 |
| scenario_table[P1/conservative/tokyo].sessions | 15 | 5 |
| scenario_table[P1/conservative/tokyo].sessions_defined | 15 | 5 |
| scenario_table[P1/intermediate/distant].mean | -11.423979454734827 | -11.429830296433707 |
| scenario_table[P1/intermediate/distant].sessions | 15 | 5 |
| scenario_table[P1/intermediate/distant].sessions_defined | 15 | 5 |
| scenario_table[P1/intermediate/regional].mean | -11.461281804136453 | -11.440181339815448 |
| scenario_table[P1/intermediate/regional].sessions | 15 | 5 |
| scenario_table[P1/intermediate/regional].sessions_defined | 15 | 5 |
| scenario_table[P1/intermediate/tokyo].mean | -11.605848963710605 | -11.567265322869403 |
| scenario_table[P1/intermediate/tokyo].sessions | 15 | 5 |
| scenario_table[P1/intermediate/tokyo].sessions_defined | 15 | 5 |
| scenario_table[P1/optimistic/distant].mean | -11.069737219626827 | -11.00354349211538 |
| scenario_table[P1/optimistic/distant].sessions | 15 | 5 |
| scenario_table[P1/optimistic/distant].sessions_defined | 15 | 5 |
| scenario_table[P1/optimistic/regional].mean | -11.139298155565045 | -11.086433004875984 |
| scenario_table[P1/optimistic/regional].sessions | 15 | 5 |
| scenario_table[P1/optimistic/regional].sessions_defined | 15 | 5 |
| scenario_table[P1/optimistic/tokyo].mean | -11.303404707913467 | -11.240807564793423 |
| scenario_table[P1/optimistic/tokyo].sessions | 15 | 5 |
| scenario_table[P1/optimistic/tokyo].sessions_defined | 15 | 5 |

Not computed on test: cap-free addendum (exploratory addendum (protocol section 11)).
Not computed on test: conditions (a), (b), h2_supported_on_discovery, material flags (interval rules needing at least 12 sessions; false by construction on 5).

## E003

State: complete. Status: forecasts observed; policies modeled historical replay; VIP0 attainable, other schedules hypothetical.

Tally (not independent replications): 3 of 3 confirmed.

| Check | Label | Discovery | Test | Status | Notes | Flag |
|---|---|---|---|---|---|---|
| H1-F | **confirmed (point estimate, 5 of 5 defined)** | 0.03644788534491028 | r2_os: mean 0.04196; 5 defined, 5 +, 0 −; t-interval (descriptive, not used) ['0.01822', '0.06569']; sessions 2026-06-01: 0.0556, 2026-07-01: 0.03127, 2026-08-01: 0.01396, 2026-09-01: 0.04883, 2026-10-01: 0.06011 | observed | mean R²_OS (M2, 5 s) > 0 (E003 §10) |  |
| H1-T | **confirmed (point estimate, 5 of 5 defined)** | -0.12382779478153157 | D_bp: mean -0.009701; 5 defined, 3 +, 2 −; t-interval (descriptive, not used) ['-0.4817', '0.4623']; sessions 2026-06-01: 0.1786, 2026-07-01: -0.4842, 2026-08-01: 0.004319, 2026-09-01: -0.2479, 2026-10-01: 0.5007 | modeled historical replay (gross, fee-free) | mean D < 0 (discovery sign) and mean D < δ = 0.5 bp (E003 §10, read literally); A not-confirmed result with 0 <= mean D < δ means only that the sign differed. It is not evidence of material translation, which would require D > δ.; gate_activity: {'P3_M2': 0.2217495260317023, 'P3_negM2': 0.26191825606817815}; sign_same_as_discovery: True; economically_immaterial_below_delta: True |  |
| H3 | **confirmed (point estimate, 5 of 5 defined)** | {'drawdown': -69.44796090624843, 'es': -3.9397619382811326, 'net_per_hour': 2.9571762606553658} | drawdown_diff: mean -19; 5 defined, 0 +, 5 −; t-interval (descriptive, not used) ['-33.4', '-4.604']; sessions 2026-06-01: -16.74, 2026-07-01: -38.91, 2026-08-01: -8.689, 2026-09-01: -14.03, 2026-10-01: -16.65<br>es_diff: mean -1.87; 5 defined, 0 +, 5 −; t-interval (descriptive, not used) ['-2.936', '-0.8035']; sessions 2026-06-01: -1.498, 2026-07-01: -2.84, 2026-08-01: -0.8044, 2026-09-01: -1.543, 2026-10-01: -2.662<br>net_per_hour_diff: mean 0.6512; 5 defined, 5 +, 0 −; t-interval (descriptive, not used) ['0.07713', '1.225']; sessions 2026-06-01: 0.6855, 2026-07-01: 1.429, 2026-08-01: 0.2472, 2026-09-01: 0.4807, 2026-10-01: 0.4136 | modeled historical replay; LP tier 4 fees are hypothetical, not attainable | mean ES diff < 0, mean drawdown diff < 0, mean net/h diff > 0 and > -δ_h (E003 §10); Passing 0.50 does not show that the risk reduction is independent of activity (A1).; delta_h: 1.1754724725329382; sign_net_per_hour_positive: True; non_inferior: True; turnover_ratio_P4_over_P3F: 0.821781507053379; partly_mechanical: False; notional_share_of_P3_M2_lp_tier4: {'P3F': 2.5521737448659394, 'P4': 2.0972865663171083} |  |

Seven policies and no-trade at VIP0 (descriptive; no label or rule). A zero for P3F or P4 is mechanical: they abstained in every discovery session at VIP0. On discovery, preferring a policy to not trading required a 99.29% interval above zero; a positive point estimate on five sessions does not show that.

| Policy | Net per hour | Discovery net per hour | vs no-trade | Gross per hour | Maker fees per hour (mechanical) | Taker fees per hour | Turnover per hour | Sessions with trades |
|---|---|---|---|---|---|---|---|---|
| P0 | -62.33 | -197.39 | -62.33 | -7.70 | 54.56 | 0.07 | 54557 | 5 |
| P1 | -55.03 | -171.01 | -55.03 | -6.85 | 48.16 | 0.03 | 48159 | 5 |
| P3F | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| P3_M1 | -24.71 | -42.10 | -24.71 | -3.37 | 21.25 | 0.08 | 21255 | 5 |
| P3_M2 | -24.79 | -42.31 | -24.79 | -3.33 | 21.38 | 0.08 | 21379 | 5 |
| P3_negM2 | -58.69 | -183.62 | -58.69 | -7.50 | 51.11 | 0.08 | 51111 | 5 |
| P4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |

| Item (reported only) | Discovery | Test |
|---|---|---|
| H1_reported.D_net_per_hour.defined | 10 | 5 |
| H1_reported.D_net_per_hour.mean | 141.30352238094537 | 33.89717081277579 |
| H1_reported.D_net_per_hour.positive | 10 | 5 |
| H1_reported.P3_M2_minus_P0_gross_bp.defined | 10 | 5 |
| H1_reported.P3_M2_minus_P0_gross_bp.mean | -0.19606817562633364 | -0.053484608746782646 |
| H1_reported.P3_M2_minus_P0_gross_bp.positive | 4 | 3 |
| H1_reported.P3_M2_minus_P0_net_per_hour.defined | 10 | 5 |
| H1_reported.P3_M2_minus_P0_net_per_hour.mean | 155.07246045011033 | 37.540063258689585 |
| H1_reported.P3_M2_minus_P0_net_per_hour.positive | 10 | 5 |
| H1_reported.P3_M2_net_per_hour_vip0.defined | 10 | 5 |
| H1_reported.P3_M2_net_per_hour_vip0.mean | -42.31453908414254 | -24.790663806477188 |
| H1_reported.P3_M2_net_per_hour_vip0.positive | 0 | 0 |
| H1_reported.ranking_P3_M2_minus_P3_M1_gross_bp.defined | 10 | 5 |
| H1_reported.ranking_P3_M2_minus_P3_M1_gross_bp.mean | -0.07333546290504896 | 0.04764265694124135 |
| H1_reported.ranking_P3_M2_minus_P3_M1_gross_bp.positive | 1 | 4 |
| H1_reported.ranking_r2_M2_minus_M1.defined | 10 | 5 |
| H1_reported.ranking_r2_M2_minus_M1.mean | 0.001344686493280911 | 0.0009561362002563411 |
| H1_reported.ranking_r2_M2_minus_M1.positive | 6 | 3 |
| H3.normalised.es_per_k_turnover_diff.defined | 10 | 5 |
| H3.normalised.es_per_k_turnover_diff.mean | -0.023097761202367267 | -0.03403922291683144 |
| H3.normalised.es_per_k_turnover_diff.positive | 0 | 0 |
| H3.normalised.inventory_per_k_turnover_diff.defined | 10 | 5 |
| H3.normalised.inventory_per_k_turnover_diff.mean | -0.03910600485885838 | -0.09450742197879002 |
| H3.normalised.inventory_per_k_turnover_diff.positive | 0 | 0 |
| H3.other_schedules.vip0.drawdown_diff.defined | 10 | 5 |
| H3.other_schedules.vip0.drawdown_diff.mean | 0.0 | 0.0 |
| H3.other_schedules.vip0.drawdown_diff.positive | 0 | 0 |
| H3.other_schedules.vip0.es_diff.defined | 10 | 5 |
| H3.other_schedules.vip0.es_diff.mean | 0.0 | 0.0 |
| H3.other_schedules.vip0.es_diff.positive | 0 | 0 |
| H3.other_schedules.vip0.net_per_hour_diff.defined | 10 | 5 |
| H3.other_schedules.vip0.net_per_hour_diff.mean | 0.0 | 0.0 |
| H3.other_schedules.vip0.net_per_hour_diff.positive | 0 | 0 |
| H3.other_schedules.vip0.not_testable_abstention | True | True |
| H3.other_schedules.vip0.notional_share_of_P3_M2.P3F | 0.0 | 0.0 |
| H3.other_schedules.vip0.notional_share_of_P3_M2.P4 | 0.0 | 0.0 |
| H3.other_schedules.vip9.drawdown_diff.defined | 10 | 5 |
| H3.other_schedules.vip9.drawdown_diff.mean | -34.29209438926845 | -14.758603699060654 |
| H3.other_schedules.vip9.drawdown_diff.positive | 0 | 0 |
| H3.other_schedules.vip9.es_diff.defined | 10 | 5 |
| H3.other_schedules.vip9.es_diff.mean | -4.193480780799648 | -1.810763885326671 |
| H3.other_schedules.vip9.es_diff.positive | 0 | 0 |
| H3.other_schedules.vip9.net_per_hour_diff.defined | 10 | 5 |
| H3.other_schedules.vip9.net_per_hour_diff.mean | 0.3831070760174067 | 0.014026619836430299 |
| H3.other_schedules.vip9.net_per_hour_diff.positive | 8 | 2 |
| H3.other_schedules.vip9.not_testable_abstention | False | False |
| H3.other_schedules.vip9.notional_share_of_P3_M2.P3F | 0.09058560932423852 | 0.046397086336551534 |
| H3.other_schedules.vip9.notional_share_of_P3_M2.P4 | 0.06672347976843958 | 0.04669493297553881 |
| P0_versus_E002.net_bp_per_notional.difference.defined | 10 | 5 |
| P0_versus_E002.net_bp_per_notional.difference.mean | 0.025114293425570543 | 0.023379924083373638 |
| P0_versus_E002.net_bp_per_notional.difference.positive | 7 | 3 |
| P0_versus_E002.net_bp_per_notional.e002_mean | -11.542121250539743 | -11.47546310358933 |
| P0_versus_E002.net_bp_per_notional.e003_mean | -11.517006957114171 | -11.452083179505959 |
| P0_versus_E002.net_per_hour.difference.defined | 10 | 5 |
| P0_versus_E002.net_per_hour.difference.mean | 33.50388935932554 | 2.7758497810802902 |
| P0_versus_E002.net_per_hour.difference.positive | 10 | 5 |
| P0_versus_E002.net_per_hour.e002_mean | -230.8908888935785 | -65.10657684624707 |
| P0_versus_E002.net_per_hour.e003_mean | -197.38699953425294 | -62.330727065166776 |
| descriptive.forecasts[M1/1].hit_rate | 0.7696540456094481 | 0.7638605557031484 |
| descriptive.forecasts[M1/1].ic | 0.2605546649542948 | 0.2472416749820039 |
| descriptive.forecasts[M1/1].mean_abs_forecast | 0.2830631746281918 | 0.21858323015899933 |
| descriptive.forecasts[M1/1].r2_os | 0.03091017844187268 | 0.050864009388828825 |
| descriptive.forecasts[M1/1].share_abs_forecast_ge_half_spread | 0.3031341651867707 | 0.026686981608283377 |
| descriptive.forecasts[M1/1].share_abs_forecast_ge_half_tick | 0.3031579263662378 | 0.026686981608283377 |
| descriptive.forecasts[M1/5].hit_rate | 0.6462794408272249 | 0.6553695172022804 |
| descriptive.forecasts[M1/5].ic | 0.20491103902767754 | 0.2096966885584874 |
| descriptive.forecasts[M1/5].mean_abs_forecast | 0.49654963197954977 | 0.38854418583978845 |
| descriptive.forecasts[M1/5].r2_os | 0.035103198851629366 | 0.04099893298079662 |
| descriptive.forecasts[M1/5].share_abs_forecast_ge_half_spread | 0.5812238304352711 | 0.2502538079151072 |
| descriptive.forecasts[M1/5].share_abs_forecast_ge_half_tick | 0.5812503561309403 | 0.25025711739160916 |
| descriptive.forecasts[M1/30].hit_rate | 0.5587412130555862 | 0.5676238793381165 |
| descriptive.forecasts[M1/30].ic | 0.11390630087612504 | 0.11706253319994944 |
| descriptive.forecasts[M1/30].mean_abs_forecast | 0.6021341660185416 | 0.492763937593195 |
| descriptive.forecasts[M1/30].r2_os | 0.014146560516036355 | 0.014139161109024823 |
| descriptive.forecasts[M1/30].share_abs_forecast_ge_half_spread | 0.6681282289257416 | 0.3759799352380642 |
| descriptive.forecasts[M1/30].share_abs_forecast_ge_half_tick | 0.6681512548014156 | 0.37598568547095695 |
| descriptive.forecasts[M2/1].hit_rate | 0.7692288615931512 | 0.7638636594359406 |
| descriptive.forecasts[M2/1].ic | 0.26323432623392834 | 0.2522252254197493 |
| descriptive.forecasts[M2/1].mean_abs_forecast | 0.28344807458662175 | 0.21213723124919034 |
| descriptive.forecasts[M2/1].r2_os | 0.040868104322455724 | 0.056888419522491726 |
| descriptive.forecasts[M2/1].share_abs_forecast_ge_half_spread | 0.3004573857734156 | 0.029318559267898735 |
| descriptive.forecasts[M2/1].share_abs_forecast_ge_half_tick | 0.3004828378604385 | 0.029319495864706623 |
| descriptive.forecasts[M2/5].hit_rate | 0.6463994536902763 | 0.6558831302222655 |
| descriptive.forecasts[M2/5].ic | 0.2054560210119687 | 0.2104474058227716 |
| descriptive.forecasts[M2/5].mean_abs_forecast | 0.49742150337065977 | 0.3793610765245722 |
| descriptive.forecasts[M2/5].r2_os | 0.03644788534491028 | 0.04195506918105296 |
| descriptive.forecasts[M2/5].share_abs_forecast_ge_half_spread | 0.5699595892452816 | 0.24058233944155108 |
| descriptive.forecasts[M2/5].share_abs_forecast_ge_half_tick | 0.5699865278149177 | 0.24058591814343777 |
| descriptive.forecasts[M2/30].hit_rate | 0.5588723149869038 | 0.5681960309289666 |
| descriptive.forecasts[M2/30].ic | 0.1136894691138866 | 0.11789849711285341 |
| descriptive.forecasts[M2/30].mean_abs_forecast | 0.6042595769585246 | 0.4833377932941502 |
| descriptive.forecasts[M2/30].r2_os | 0.014106040643452533 | 0.01426386324468316 |
| descriptive.forecasts[M2/30].share_abs_forecast_ge_half_spread | 0.6587812596098521 | 0.36452043738923 |
| descriptive.forecasts[M2/30].share_abs_forecast_ge_half_tick | 0.6588052755650146 | 0.36452582336230205 |
| descriptive.scenarios[NT/none/none/lp_tier4].fill_rate | None | undefined |
| descriptive.scenarios[NT/none/none/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[NT/none/none/lp_tier4].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[NT/none/none/lp_tier4].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].net_bp_per_notional | None | undefined |
| descriptive.scenarios[NT/none/none/lp_tier4].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[NT/none/none/lp_tier4].orders_per_fill | None | undefined |
| descriptive.scenarios[NT/none/none/lp_tier4].own_edge_bp | None | undefined |
| descriptive.scenarios[NT/none/none/lp_tier4].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[NT/none/none/lp_tier4].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[NT/none/none/lp_tier4].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[NT/none/none/lp_tier4].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[NT/none/none/lp_tier4].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[NT/none/none/vip0].fill_rate | None | undefined |
| descriptive.scenarios[NT/none/none/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[NT/none/none/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[NT/none/none/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[NT/none/none/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[NT/none/none/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[NT/none/none/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[NT/none/none/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[NT/none/none/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[NT/none/none/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[NT/none/none/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].sessions | 10 | 5 |
| descriptive.scenarios[NT/none/none/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[NT/none/none/vip9].fill_rate | None | undefined |
| descriptive.scenarios[NT/none/none/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[NT/none/none/vip9].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[NT/none/none/vip9].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].net_bp_per_notional | None | undefined |
| descriptive.scenarios[NT/none/none/vip9].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[NT/none/none/vip9].orders_per_fill | None | undefined |
| descriptive.scenarios[NT/none/none/vip9].own_edge_bp | None | undefined |
| descriptive.scenarios[NT/none/none/vip9].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[NT/none/none/vip9].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[NT/none/none/vip9].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[NT/none/none/vip9].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].sessions | 10 | 5 |
| descriptive.scenarios[NT/none/none/vip9].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[NT/none/none/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].fill_rate | 0.2886843513150262 | 0.2527208275640717 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].gross_bp_per_notional | -1.6406794107445033 | -1.6225467157075042 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].gross_per_hour | -18.93059794487325 | -6.120964304303366 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].inc_es | 6.347998340195256 | 3.021887453343707 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].inc_std | 1.977165065953789 | 0.9782534097709163 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].inc_worst | -13.645532636280171 | -4.7978427139200015 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].liquidation_shortfall | 0.46300000000000574 | 0.0 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].max_abs_inventory | 10.703399999999395 | 10.738600000000059 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].max_drawdown | 219.84450051309673 | 77.45454026368304 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].net_bp_per_notional | -0.8432270941322166 | -0.8292555753124956 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].net_per_hour | -9.791632545488 | -3.0921486296159535 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].net_per_hour_over_inc_std | -4.258677558541978 | -2.943218053520913 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].orders_per_fill | 0.55368734827842 | 0.829736032109569 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].own_edge_bp | 0.19887970415602746 | 0.22032414562290992 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].own_markout_1s_bp | -1.327670553878247 | -1.3935078643926393 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].own_markout_30s_bp | -1.635971704749896 | -1.6518621827994977 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].own_markout_5s_bp | -1.5371740117905526 | -1.5860229110536408 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].paced_spells | 7066.6 | 1374.6 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].paced_time_share | 0.02296226726124334 | 0.004025750772733658 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].quote_presence_ask | 0.8610199589654467 | 0.8833023237180173 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].quote_presence_bid | 0.8610861222688193 | 0.9124113342498255 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].quote_presence_both | 0.7467934642490344 | 0.8036821947063014 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].turnover_per_hour | 114591.1020012765 | 38092.34496771199 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].tw_abs_inventory_avg | 5.63752896016183 | 5.617832556616072 |
| descriptive.scenarios[P0/conservative/distant/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/conservative/distant/vip0].fill_rate | 0.2886843513150262 | 0.2527208275640717 |
| descriptive.scenarios[P0/conservative/distant/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P0/conservative/distant/vip0].gross_bp_per_notional | -1.6406794107445033 | -1.6225467157075042 |
| descriptive.scenarios[P0/conservative/distant/vip0].gross_per_hour | -18.93059794487325 | -6.120964304303366 |
| descriptive.scenarios[P0/conservative/distant/vip0].inc_es | 23.409199857505307 | 11.424567910799842 |
| descriptive.scenarios[P0/conservative/distant/vip0].inc_std | 4.92484510126007 | 2.631961710173551 |
| descriptive.scenarios[P0/conservative/distant/vip0].inc_worst | -31.958210766995865 | -15.891578261998845 |
| descriptive.scenarios[P0/conservative/distant/vip0].liquidation_shortfall | 0.46300000000000574 | 0.0 |
| descriptive.scenarios[P0/conservative/distant/vip0].max_abs_inventory | 10.703399999999395 | 10.738600000000059 |
| descriptive.scenarios[P0/conservative/distant/vip0].max_drawdown | 2921.112944335647 | 1060.9089368880245 |
| descriptive.scenarios[P0/conservative/distant/vip0].net_bp_per_notional | -11.65175629503891 | -11.651715670511816 |
| descriptive.scenarios[P0/conservative/distant/vip0].net_per_hour | -133.64484238404918 | -44.294056762143825 |
| descriptive.scenarios[P0/conservative/distant/vip0].net_per_hour_over_inc_std | -23.820013578994338 | -15.711066382681276 |
| descriptive.scenarios[P0/conservative/distant/vip0].orders_per_fill | 0.55368734827842 | 0.829736032109569 |
| descriptive.scenarios[P0/conservative/distant/vip0].own_edge_bp | 0.19887970415602746 | 0.22032414562290992 |
| descriptive.scenarios[P0/conservative/distant/vip0].own_markout_1s_bp | -1.327670553878247 | -1.3935078643926393 |
| descriptive.scenarios[P0/conservative/distant/vip0].own_markout_30s_bp | -1.635971704749896 | -1.6518621827994977 |
| descriptive.scenarios[P0/conservative/distant/vip0].own_markout_5s_bp | -1.5371740117905526 | -1.5860229110536408 |
| descriptive.scenarios[P0/conservative/distant/vip0].paced_spells | 7066.6 | 1374.6 |
| descriptive.scenarios[P0/conservative/distant/vip0].paced_time_share | 0.02296226726124334 | 0.004025750772733658 |
| descriptive.scenarios[P0/conservative/distant/vip0].quote_presence_ask | 0.8610199589654467 | 0.8833023237180173 |
| descriptive.scenarios[P0/conservative/distant/vip0].quote_presence_bid | 0.8610861222688193 | 0.9124113342498255 |
| descriptive.scenarios[P0/conservative/distant/vip0].quote_presence_both | 0.7467934642490344 | 0.8036821947063014 |
| descriptive.scenarios[P0/conservative/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P0/conservative/distant/vip0].turnover_per_hour | 114591.1020012765 | 38092.34496771199 |
| descriptive.scenarios[P0/conservative/distant/vip0].tw_abs_inventory_avg | 5.63752896016183 | 5.617832556616072 |
| descriptive.scenarios[P0/conservative/distant/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/conservative/distant/vip9].fill_rate | 0.2886843513150262 | 0.2527208275640717 |
| descriptive.scenarios[P0/conservative/distant/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P0/conservative/distant/vip9].gross_bp_per_notional | -1.6406794107445033 | -1.6225467157075042 |
| descriptive.scenarios[P0/conservative/distant/vip9].gross_per_hour | -18.93059794487325 | -6.120964304303366 |
| descriptive.scenarios[P0/conservative/distant/vip9].inc_es | 8.904202000602485 | 4.211136289523829 |
| descriptive.scenarios[P0/conservative/distant/vip9].inc_std | 2.1965134255170766 | 1.1355328823208903 |
| descriptive.scenarios[P0/conservative/distant/vip9].inc_worst | -16.543168580309665 | -6.177181731080176 |
| descriptive.scenarios[P0/conservative/distant/vip9].liquidation_shortfall | 0.46300000000000574 | 0.0 |
| descriptive.scenarios[P0/conservative/distant/vip9].max_abs_inventory | 10.703399999999395 | 10.738600000000059 |
| descriptive.scenarios[P0/conservative/distant/vip9].max_drawdown | 692.8957745487534 | 247.9768337957492 |
| descriptive.scenarios[P0/conservative/distant/vip9].net_bp_per_notional | -2.7432270941322168 | -2.7292555753124956 |
| descriptive.scenarios[P0/conservative/distant/vip9].net_per_hour | -31.563941925730536 | -10.329694173481233 |
| descriptive.scenarios[P0/conservative/distant/vip9].net_per_hour_over_inc_std | -12.515583753111791 | -8.424345979446683 |
| descriptive.scenarios[P0/conservative/distant/vip9].orders_per_fill | 0.55368734827842 | 0.829736032109569 |
| descriptive.scenarios[P0/conservative/distant/vip9].own_edge_bp | 0.19887970415602746 | 0.22032414562290992 |
| descriptive.scenarios[P0/conservative/distant/vip9].own_markout_1s_bp | -1.327670553878247 | -1.3935078643926393 |
| descriptive.scenarios[P0/conservative/distant/vip9].own_markout_30s_bp | -1.635971704749896 | -1.6518621827994977 |
| descriptive.scenarios[P0/conservative/distant/vip9].own_markout_5s_bp | -1.5371740117905526 | -1.5860229110536408 |
| descriptive.scenarios[P0/conservative/distant/vip9].paced_spells | 7066.6 | 1374.6 |
| descriptive.scenarios[P0/conservative/distant/vip9].paced_time_share | 0.02296226726124334 | 0.004025750772733658 |
| descriptive.scenarios[P0/conservative/distant/vip9].quote_presence_ask | 0.8610199589654467 | 0.8833023237180173 |
| descriptive.scenarios[P0/conservative/distant/vip9].quote_presence_bid | 0.8610861222688193 | 0.9124113342498255 |
| descriptive.scenarios[P0/conservative/distant/vip9].quote_presence_both | 0.7467934642490344 | 0.8036821947063014 |
| descriptive.scenarios[P0/conservative/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P0/conservative/distant/vip9].turnover_per_hour | 114591.1020012765 | 38092.34496771199 |
| descriptive.scenarios[P0/conservative/distant/vip9].tw_abs_inventory_avg | 5.63752896016183 | 5.617832556616072 |
| descriptive.scenarios[P0/conservative/distant/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].fill_rate | 0.2902353544152872 | 0.23964370235381813 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].gross_bp_per_notional | -1.6513847995966224 | -1.657996846999256 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].gross_per_hour | -23.692204848225728 | -6.757839805301094 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].inc_es | 6.595370824486267 | 3.1852070903359193 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].inc_std | 2.0017439635213194 | 1.0115952308811131 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].inc_worst | -12.704106622081468 | -4.87121892991995 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].liquidation_shortfall | 0.5447000000000054 | 0.0 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].max_abs_inventory | 10.804600000000587 | 10.59280000000005 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].max_drawdown | 275.3038949999358 | 86.92014193420327 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].net_bp_per_notional | -0.8536234686450795 | -0.8646093563766513 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].net_per_hour | -12.325698672870626 | -3.4978462496356357 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].net_per_hour_over_inc_std | -5.22755514829293 | -3.210472399212815 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].orders_per_fill | 0.49634990252564587 | 0.8189529220183553 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].own_edge_bp | 0.16982658522069755 | 0.24654770181355215 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].own_markout_1s_bp | -1.3876326381570565 | -1.436123974710812 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].own_markout_30s_bp | -1.6698111310925825 | -1.686695056499638 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].own_markout_5s_bp | -1.5800049588464062 | -1.625497323626141 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].paced_spells | 7635.2 | 1374.0 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].paced_time_share | 0.025031371896506317 | 0.004010367813103111 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].quote_presence_ask | 0.8762720477567945 | 0.8791243394130659 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].quote_presence_bid | 0.8704936580590539 | 0.9132219859146178 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].quote_presence_both | 0.7680542117583125 | 0.7987040879655136 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].turnover_per_hour | 142498.27603569947 | 40987.90014810428 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].tw_abs_inventory_avg | 5.6408800099545084 | 5.660653883341705 |
| descriptive.scenarios[P0/conservative/regional/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/conservative/regional/vip0].fill_rate | 0.2902353544152872 | 0.23964370235381813 |
| descriptive.scenarios[P0/conservative/regional/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P0/conservative/regional/vip0].gross_bp_per_notional | -1.6513847995966224 | -1.657996846999256 |
| descriptive.scenarios[P0/conservative/regional/vip0].gross_per_hour | -23.692204848225728 | -6.757839805301094 |
| descriptive.scenarios[P0/conservative/regional/vip0].inc_es | 30.060074724931617 | 12.809973545733646 |
| descriptive.scenarios[P0/conservative/regional/vip0].inc_std | 6.391409942934455 | 2.980694228295748 |
| descriptive.scenarios[P0/conservative/regional/vip0].inc_worst | -41.95001139198764 | -19.516992851998687 |
| descriptive.scenarios[P0/conservative/regional/vip0].liquidation_shortfall | 0.5447000000000054 | 0.0 |
| descriptive.scenarios[P0/conservative/regional/vip0].max_abs_inventory | 10.804600000000587 | 10.59280000000005 |
| descriptive.scenarios[P0/conservative/regional/vip0].max_drawdown | 3618.020709977707 | 1145.6569979500423 |
| descriptive.scenarios[P0/conservative/regional/vip0].net_bp_per_notional | -11.661118143285567 | -11.68674688777054 |
| descriptive.scenarios[P0/conservative/regional/vip0].net_per_hour | -166.3355065687115 | -47.8285158498527 |
| descriptive.scenarios[P0/conservative/regional/vip0].net_per_hour_over_inc_std | -22.731817297208632 | -14.933162143949307 |
| descriptive.scenarios[P0/conservative/regional/vip0].orders_per_fill | 0.49634990252564587 | 0.8189529220183553 |
| descriptive.scenarios[P0/conservative/regional/vip0].own_edge_bp | 0.16982658522069755 | 0.24654770181355215 |
| descriptive.scenarios[P0/conservative/regional/vip0].own_markout_1s_bp | -1.3876326381570565 | -1.436123974710812 |
| descriptive.scenarios[P0/conservative/regional/vip0].own_markout_30s_bp | -1.6698111310925825 | -1.686695056499638 |
| descriptive.scenarios[P0/conservative/regional/vip0].own_markout_5s_bp | -1.5800049588464062 | -1.625497323626141 |
| descriptive.scenarios[P0/conservative/regional/vip0].paced_spells | 7635.2 | 1374.0 |
| descriptive.scenarios[P0/conservative/regional/vip0].paced_time_share | 0.025031371896506317 | 0.004010367813103111 |
| descriptive.scenarios[P0/conservative/regional/vip0].quote_presence_ask | 0.8762720477567945 | 0.8791243394130659 |
| descriptive.scenarios[P0/conservative/regional/vip0].quote_presence_bid | 0.8704936580590539 | 0.9132219859146178 |
| descriptive.scenarios[P0/conservative/regional/vip0].quote_presence_both | 0.7680542117583125 | 0.7987040879655136 |
| descriptive.scenarios[P0/conservative/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P0/conservative/regional/vip0].turnover_per_hour | 142498.27603569947 | 40987.90014810428 |
| descriptive.scenarios[P0/conservative/regional/vip0].tw_abs_inventory_avg | 5.6408800099545084 | 5.660653883341705 |
| descriptive.scenarios[P0/conservative/regional/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/conservative/regional/vip9].fill_rate | 0.2902353544152872 | 0.23964370235381813 |
| descriptive.scenarios[P0/conservative/regional/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P0/conservative/regional/vip9].gross_bp_per_notional | -1.6513847995966224 | -1.657996846999256 |
| descriptive.scenarios[P0/conservative/regional/vip9].gross_per_hour | -23.692204848225728 | -6.757839805301094 |
| descriptive.scenarios[P0/conservative/regional/vip9].inc_es | 10.111193792483457 | 4.571274602894772 |
| descriptive.scenarios[P0/conservative/regional/vip9].inc_std | 2.419046522806116 | 1.2144565599242383 |
| descriptive.scenarios[P0/conservative/regional/vip9].inc_worst | -17.2112212414379 | -7.01393657979952 |
| descriptive.scenarios[P0/conservative/regional/vip9].liquidation_shortfall | 0.5447000000000054 | 0.0 |
| descriptive.scenarios[P0/conservative/regional/vip9].max_abs_inventory | 10.804600000000587 | 10.59280000000005 |
| descriptive.scenarios[P0/conservative/regional/vip9].max_drawdown | 860.729390646438 | 270.76170105265186 |
| descriptive.scenarios[P0/conservative/regional/vip9].net_bp_per_notional | -2.75362346864508 | -2.7646093563766514 |
| descriptive.scenarios[P0/conservative/regional/vip9].net_per_hour | -39.40037111965352 | -11.28554727777545 |
| descriptive.scenarios[P0/conservative/regional/vip9].net_per_hour_over_inc_std | -14.005320730210375 | -8.60265673117083 |
| descriptive.scenarios[P0/conservative/regional/vip9].orders_per_fill | 0.49634990252564587 | 0.8189529220183553 |
| descriptive.scenarios[P0/conservative/regional/vip9].own_edge_bp | 0.16982658522069755 | 0.24654770181355215 |
| descriptive.scenarios[P0/conservative/regional/vip9].own_markout_1s_bp | -1.3876326381570565 | -1.436123974710812 |
| descriptive.scenarios[P0/conservative/regional/vip9].own_markout_30s_bp | -1.6698111310925825 | -1.686695056499638 |
| descriptive.scenarios[P0/conservative/regional/vip9].own_markout_5s_bp | -1.5800049588464062 | -1.625497323626141 |
| descriptive.scenarios[P0/conservative/regional/vip9].paced_spells | 7635.2 | 1374.0 |
| descriptive.scenarios[P0/conservative/regional/vip9].paced_time_share | 0.025031371896506317 | 0.004010367813103111 |
| descriptive.scenarios[P0/conservative/regional/vip9].quote_presence_ask | 0.8762720477567945 | 0.8791243394130659 |
| descriptive.scenarios[P0/conservative/regional/vip9].quote_presence_bid | 0.8704936580590539 | 0.9132219859146178 |
| descriptive.scenarios[P0/conservative/regional/vip9].quote_presence_both | 0.7680542117583125 | 0.7987040879655136 |
| descriptive.scenarios[P0/conservative/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P0/conservative/regional/vip9].turnover_per_hour | 142498.27603569947 | 40987.90014810428 |
| descriptive.scenarios[P0/conservative/regional/vip9].tw_abs_inventory_avg | 5.6408800099545084 | 5.660653883341705 |
| descriptive.scenarios[P0/conservative/regional/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].fill_rate | 0.29510984383306216 | 0.22078798577810507 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].gross_bp_per_notional | -1.8559428669255582 | -1.904243084424635 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].gross_per_hour | -28.858912124655014 | -7.730059594273532 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].inc_es | 6.815245490138892 | 3.3527148700159266 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].inc_std | 2.0445648767036966 | 1.051235020676009 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].inc_worst | -12.00382296840006 | -5.300795465280677 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].liquidation_shortfall | 0.475800000000007 | 0.0 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].max_abs_inventory | 10.353600000000203 | 10.050000000000107 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].max_drawdown | 357.50945158658396 | 108.27473648159844 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].net_bp_per_notional | -1.0578069001540753 | -1.110203354462983 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].net_per_hour | -16.19639776328893 | -4.431743662730415 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].net_per_hour_over_inc_std | -6.925103878821718 | -3.9408762374832165 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].orders_per_fill | 0.4869240423963568 | 0.8814507851724456 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].own_edge_bp | 0.34435854684514366 | 0.5110631906892608 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].own_markout_1s_bp | -1.6222576107771407 | -1.6436441018164771 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].own_markout_30s_bp | -1.8967495952043218 | -1.8737684398375716 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].own_markout_5s_bp | -1.8072018175007956 | -1.8160049647129461 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].paced_spells | 7930.6 | 1507.6 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].paced_time_share | 0.026032238693341963 | 0.00442417753256222 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].quote_presence_ask | 0.870799308376397 | 0.8879938526814286 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].quote_presence_bid | 0.8429937573635025 | 0.8972839934926752 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].quote_presence_both | 0.7341195290737692 | 0.7913771526963507 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].turnover_per_hour | 158695.9445228811 | 41432.31594190108 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].tw_abs_inventory_avg | 5.913154083428385 | 5.777174240699835 |
| descriptive.scenarios[P0/conservative/tokyo/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/conservative/tokyo/vip0].fill_rate | 0.29510984383306216 | 0.22078798577810507 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P0/conservative/tokyo/vip0].gross_bp_per_notional | -1.8559428669255582 | -1.904243084424635 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].gross_per_hour | -28.858912124655014 | -7.730059594273532 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].inc_es | 32.60214612069695 | 12.673078621733563 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].inc_std | 6.9427692658902505 | 2.988953529952498 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].inc_worst | -43.052492630999026 | -18.788942697998884 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].liquidation_shortfall | 0.475800000000007 | 0.0 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].max_abs_inventory | 10.353600000000203 | 10.050000000000107 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].max_drawdown | 4071.8238500327266 | 1179.43888979605 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].net_bp_per_notional | -11.86404735922346 | -11.930157301982671 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].net_per_hour | -187.69903577999003 | -49.23311181360492 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].net_per_hour_over_inc_std | -23.641827636673117 | -15.167113751825838 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].orders_per_fill | 0.4869240423963568 | 0.8814507851724456 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].own_edge_bp | 0.34435854684514366 | 0.5110631906892608 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].own_markout_1s_bp | -1.6222576107771407 | -1.6436441018164771 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].own_markout_30s_bp | -1.8967495952043218 | -1.8737684398375716 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].own_markout_5s_bp | -1.8072018175007956 | -1.8160049647129461 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].paced_spells | 7930.6 | 1507.6 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].paced_time_share | 0.026032238693341963 | 0.00442417753256222 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].quote_presence_ask | 0.870799308376397 | 0.8879938526814286 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].quote_presence_bid | 0.8429937573635025 | 0.8972839934926752 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].quote_presence_both | 0.7341195290737692 | 0.7913771526963507 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].turnover_per_hour | 158695.9445228811 | 41432.31594190108 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].tw_abs_inventory_avg | 5.913154083428385 | 5.777174240699835 |
| descriptive.scenarios[P0/conservative/tokyo/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/conservative/tokyo/vip9].fill_rate | 0.29510984383306216 | 0.22078798577810507 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P0/conservative/tokyo/vip9].gross_bp_per_notional | -1.8559428669255582 | -1.904243084424635 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].gross_per_hour | -28.858912124655014 | -7.730059594273532 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].inc_es | 10.76528909967455 | 4.772802607162721 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].inc_std | 2.5525217850669333 | 1.2534819964579493 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].inc_worst | -16.62804156826 | -7.179726942700614 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].liquidation_shortfall | 0.475800000000007 | 0.0 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].max_abs_inventory | 10.353600000000203 | 10.050000000000107 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].max_drawdown | 1009.4606016779741 | 295.0332887308019 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].net_bp_per_notional | -2.9578069001540754 | -3.010203354462983 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].net_per_hour | -46.348627222636345 | -12.30388369169162 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].net_per_hour_over_inc_std | -15.72538271707736 | -9.075340098759208 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].orders_per_fill | 0.4869240423963568 | 0.8814507851724456 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].own_edge_bp | 0.34435854684514366 | 0.5110631906892608 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].own_markout_1s_bp | -1.6222576107771407 | -1.6436441018164771 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].own_markout_30s_bp | -1.8967495952043218 | -1.8737684398375716 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].own_markout_5s_bp | -1.8072018175007956 | -1.8160049647129461 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].paced_spells | 7930.6 | 1507.6 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].paced_time_share | 0.026032238693341963 | 0.00442417753256222 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].quote_presence_ask | 0.870799308376397 | 0.8879938526814286 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].quote_presence_bid | 0.8429937573635025 | 0.8972839934926752 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].quote_presence_both | 0.7341195290737692 | 0.7913771526963507 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].turnover_per_hour | 158695.9445228811 | 41432.31594190108 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].tw_abs_inventory_avg | 5.913154083428385 | 5.777174240699835 |
| descriptive.scenarios[P0/conservative/tokyo/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].fill_rate | 0.34055800926560365 | 0.3118787259989175 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].gross_bp_per_notional | -1.4523727517083582 | -1.4322496989631763 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].gross_per_hour | -19.712788151068313 | -6.697626618885302 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].inc_es | 6.235699235685752 | 2.991350472799983 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].inc_std | 1.953813792683739 | 0.968213003812977 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].inc_worst | -13.65360235927964 | -4.710584223680278 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].liquidation_shortfall | 0.45480000000000215 | 0.0 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].max_abs_inventory | 10.638900000000353 | 10.753400000000108 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].max_drawdown | 205.45691128273702 | 74.75740248603833 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].net_bp_per_notional | -0.6543731850637408 | -0.6369049211300364 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].net_per_hour | -9.104305715029366 | -2.893664618850791 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].net_per_hour_over_inc_std | -3.9832800713401406 | -2.8416690329348677 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].orders_per_fill | 0.6077008803955749 | 0.888764759788536 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].own_edge_bp | 0.2738498435753064 | 0.3533713594499914 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].own_markout_1s_bp | -1.1153772674067952 | -1.1177922721219933 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].own_markout_30s_bp | -1.4371381211883938 | -1.3920268440834773 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].own_markout_5s_bp | -1.3229090508877708 | -1.3228684955138137 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].paced_spells | 7495.2 | 1598.0 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].paced_time_share | 0.024314974265601346 | 0.004664621966617389 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].quote_presence_ask | 0.8513467140815578 | 0.8891020196229802 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].quote_presence_bid | 0.868769883211311 | 0.8922956917905406 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].quote_presence_both | 0.7461379734027104 | 0.79022811445471 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].turnover_per_hour | 132967.5381255522 | 47750.20895024877 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].tw_abs_inventory_avg | 5.44156056076951 | 5.570991992141417 |
| descriptive.scenarios[P0/intermediate/distant/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/intermediate/distant/vip0].fill_rate | 0.34055800926560365 | 0.3118787259989175 |
| descriptive.scenarios[P0/intermediate/distant/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P0/intermediate/distant/vip0].gross_bp_per_notional | -1.4523727517083582 | -1.4322496989631763 |
| descriptive.scenarios[P0/intermediate/distant/vip0].gross_per_hour | -19.712788151068313 | -6.697626618885302 |
| descriptive.scenarios[P0/intermediate/distant/vip0].inc_es | 24.671946518340214 | 12.639715607067071 |
| descriptive.scenarios[P0/intermediate/distant/vip0].inc_std | 4.941248784289171 | 2.818938563931732 |
| descriptive.scenarios[P0/intermediate/distant/vip0].inc_worst | -32.56844966799841 | -17.08613223200025 |
| descriptive.scenarios[P0/intermediate/distant/vip0].liquidation_shortfall | 0.45480000000000215 | 0.0 |
| descriptive.scenarios[P0/intermediate/distant/vip0].max_abs_inventory | 10.638900000000353 | 10.753400000000108 |
| descriptive.scenarios[P0/intermediate/distant/vip0].max_drawdown | 3342.699367001751 | 1305.6538069320316 |
| descriptive.scenarios[P0/intermediate/distant/vip0].net_bp_per_notional | -11.461070288036108 | -11.452489795340831 |
| descriptive.scenarios[P0/intermediate/distant/vip0].net_per_hour | -152.80606807664327 | -54.51763868211403 |
| descriptive.scenarios[P0/intermediate/distant/vip0].net_per_hour_over_inc_std | -27.60984624348297 | -18.177996478525195 |
| descriptive.scenarios[P0/intermediate/distant/vip0].orders_per_fill | 0.6077008803955749 | 0.888764759788536 |
| descriptive.scenarios[P0/intermediate/distant/vip0].own_edge_bp | 0.2738498435753064 | 0.3533713594499914 |
| descriptive.scenarios[P0/intermediate/distant/vip0].own_markout_1s_bp | -1.1153772674067952 | -1.1177922721219933 |
| descriptive.scenarios[P0/intermediate/distant/vip0].own_markout_30s_bp | -1.4371381211883938 | -1.3920268440834773 |
| descriptive.scenarios[P0/intermediate/distant/vip0].own_markout_5s_bp | -1.3229090508877708 | -1.3228684955138137 |
| descriptive.scenarios[P0/intermediate/distant/vip0].paced_spells | 7495.2 | 1598.0 |
| descriptive.scenarios[P0/intermediate/distant/vip0].paced_time_share | 0.024314974265601346 | 0.004664621966617389 |
| descriptive.scenarios[P0/intermediate/distant/vip0].quote_presence_ask | 0.8513467140815578 | 0.8891020196229802 |
| descriptive.scenarios[P0/intermediate/distant/vip0].quote_presence_bid | 0.868769883211311 | 0.8922956917905406 |
| descriptive.scenarios[P0/intermediate/distant/vip0].quote_presence_both | 0.7461379734027104 | 0.79022811445471 |
| descriptive.scenarios[P0/intermediate/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P0/intermediate/distant/vip0].turnover_per_hour | 132967.5381255522 | 47750.20895024877 |
| descriptive.scenarios[P0/intermediate/distant/vip0].tw_abs_inventory_avg | 5.44156056076951 | 5.570991992141417 |
| descriptive.scenarios[P0/intermediate/distant/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/intermediate/distant/vip9].fill_rate | 0.34055800926560365 | 0.3118787259989175 |
| descriptive.scenarios[P0/intermediate/distant/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P0/intermediate/distant/vip9].gross_bp_per_notional | -1.4523727517083582 | -1.4322496989631763 |
| descriptive.scenarios[P0/intermediate/distant/vip9].gross_per_hour | -19.712788151068313 | -6.697626618885302 |
| descriptive.scenarios[P0/intermediate/distant/vip9].inc_es | 8.975092452229273 | 4.3638980881787734 |
| descriptive.scenarios[P0/intermediate/distant/vip9].inc_std | 2.160314589543382 | 1.1394235838960693 |
| descriptive.scenarios[P0/intermediate/distant/vip9].inc_worst | -16.736673318489032 | -6.159176640420268 |
| descriptive.scenarios[P0/intermediate/distant/vip9].liquidation_shortfall | 0.45480000000000215 | 0.0 |
| descriptive.scenarios[P0/intermediate/distant/vip9].max_abs_inventory | 10.638900000000353 | 10.753400000000108 |
| descriptive.scenarios[P0/intermediate/distant/vip9].max_drawdown | 754.7277736511344 | 286.94615812422603 |
| descriptive.scenarios[P0/intermediate/distant/vip9].net_bp_per_notional | -2.5543731850637412 | -2.5369049211300365 |
| descriptive.scenarios[P0/intermediate/distant/vip9].net_per_hour | -34.36813795888429 | -11.966204319398056 |
| descriptive.scenarios[P0/intermediate/distant/vip9].net_per_hour_over_inc_std | -14.087665295680003 | -9.829702876663525 |
| descriptive.scenarios[P0/intermediate/distant/vip9].orders_per_fill | 0.6077008803955749 | 0.888764759788536 |
| descriptive.scenarios[P0/intermediate/distant/vip9].own_edge_bp | 0.2738498435753064 | 0.3533713594499914 |
| descriptive.scenarios[P0/intermediate/distant/vip9].own_markout_1s_bp | -1.1153772674067952 | -1.1177922721219933 |
| descriptive.scenarios[P0/intermediate/distant/vip9].own_markout_30s_bp | -1.4371381211883938 | -1.3920268440834773 |
| descriptive.scenarios[P0/intermediate/distant/vip9].own_markout_5s_bp | -1.3229090508877708 | -1.3228684955138137 |
| descriptive.scenarios[P0/intermediate/distant/vip9].paced_spells | 7495.2 | 1598.0 |
| descriptive.scenarios[P0/intermediate/distant/vip9].paced_time_share | 0.024314974265601346 | 0.004664621966617389 |
| descriptive.scenarios[P0/intermediate/distant/vip9].quote_presence_ask | 0.8513467140815578 | 0.8891020196229802 |
| descriptive.scenarios[P0/intermediate/distant/vip9].quote_presence_bid | 0.868769883211311 | 0.8922956917905406 |
| descriptive.scenarios[P0/intermediate/distant/vip9].quote_presence_both | 0.7461379734027104 | 0.79022811445471 |
| descriptive.scenarios[P0/intermediate/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P0/intermediate/distant/vip9].turnover_per_hour | 132967.5381255522 | 47750.20895024877 |
| descriptive.scenarios[P0/intermediate/distant/vip9].tw_abs_inventory_avg | 5.44156056076951 | 5.570991992141417 |
| descriptive.scenarios[P0/intermediate/distant/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].fill_rate | 0.3447061432189926 | 0.30256289210734033 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].gross_bp_per_notional | -1.5097047231221425 | -1.4330080502894866 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].gross_per_hour | -26.090585369861316 | -7.701392778650965 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].inc_es | 6.643685138353144 | 3.165202266303666 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].inc_std | 2.013189818400558 | 0.9976080930804792 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].inc_worst | -12.658788309641007 | -4.977537540799746 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].liquidation_shortfall | 0.5005999999999992 | 0.0 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].max_abs_inventory | 10.820099999999808 | 10.754000000000017 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].max_drawdown | 277.65900113570376 | 84.16699075263982 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].net_bp_per_notional | -0.7113842369403092 | -0.6373953300092753 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].net_per_hour | -12.430211098055088 | -3.3535883963404145 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].net_per_hour_over_inc_std | -5.297855100950571 | -3.170642495405804 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].orders_per_fill | 0.5113944690530897 | 0.8146066418163931 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].own_edge_bp | 0.22858500966316422 | 0.34244483305412293 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].own_markout_1s_bp | -1.1796616501855328 | -1.1663852891053672 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].own_markout_30s_bp | -1.4763560368261688 | -1.430623272880284 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].own_markout_5s_bp | -1.3681306937037538 | -1.3658665144869295 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].paced_spells | 8265.6 | 1678.2 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].paced_time_share | 0.02697022768744426 | 0.004917302495383665 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].quote_presence_ask | 0.8743528337466449 | 0.8931723502917684 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].quote_presence_bid | 0.8830280479877681 | 0.9053593777282364 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].quote_presence_both | 0.7793790708053236 | 0.8055197431950052 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].turnover_per_hour | 171156.61138585903 | 54556.616994223186 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].tw_abs_inventory_avg | 5.426336611367309 | 5.539076138269047 |
| descriptive.scenarios[P0/intermediate/regional/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/intermediate/regional/vip0].fill_rate | 0.3447061432189926 | 0.30256289210734033 |
| descriptive.scenarios[P0/intermediate/regional/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P0/intermediate/regional/vip0].gross_bp_per_notional | -1.5097047231221425 | -1.4330080502894866 |
| descriptive.scenarios[P0/intermediate/regional/vip0].gross_per_hour | -26.090585369861316 | -7.701392778650965 |
| descriptive.scenarios[P0/intermediate/regional/vip0].inc_es | 32.419186583017606 | 14.85735220653369 |
| descriptive.scenarios[P0/intermediate/regional/vip0].inc_std | 6.5832297886457924 | 3.3509595387614284 |
| descriptive.scenarios[P0/intermediate/regional/vip0].inc_worst | -43.19566232398853 | -21.25428747999961 |
| descriptive.scenarios[P0/intermediate/regional/vip0].liquidation_shortfall | 0.5005999999999992 | 0.0 |
| descriptive.scenarios[P0/intermediate/regional/vip0].max_abs_inventory | 10.820099999999808 | 10.754000000000017 |
| descriptive.scenarios[P0/intermediate/regional/vip0].max_drawdown | 4299.824089768761 | 1492.8247944860366 |
| descriptive.scenarios[P0/intermediate/regional/vip0].net_bp_per_notional | -11.517006957114173 | -11.452083179505959 |
| descriptive.scenarios[P0/intermediate/regional/vip0].net_per_hour | -197.3869995342529 | -62.330727065166776 |
| descriptive.scenarios[P0/intermediate/regional/vip0].net_per_hour_over_inc_std | -26.686829051566797 | -17.410442952666298 |
| descriptive.scenarios[P0/intermediate/regional/vip0].orders_per_fill | 0.5113944690530897 | 0.8146066418163931 |
| descriptive.scenarios[P0/intermediate/regional/vip0].own_edge_bp | 0.22858500966316422 | 0.34244483305412293 |
| descriptive.scenarios[P0/intermediate/regional/vip0].own_markout_1s_bp | -1.1796616501855328 | -1.1663852891053672 |
| descriptive.scenarios[P0/intermediate/regional/vip0].own_markout_30s_bp | -1.4763560368261688 | -1.430623272880284 |
| descriptive.scenarios[P0/intermediate/regional/vip0].own_markout_5s_bp | -1.3681306937037538 | -1.3658665144869295 |
| descriptive.scenarios[P0/intermediate/regional/vip0].paced_spells | 8265.6 | 1678.2 |
| descriptive.scenarios[P0/intermediate/regional/vip0].paced_time_share | 0.02697022768744426 | 0.004917302495383665 |
| descriptive.scenarios[P0/intermediate/regional/vip0].quote_presence_ask | 0.8743528337466449 | 0.8931723502917684 |
| descriptive.scenarios[P0/intermediate/regional/vip0].quote_presence_bid | 0.8830280479877681 | 0.9053593777282364 |
| descriptive.scenarios[P0/intermediate/regional/vip0].quote_presence_both | 0.7793790708053236 | 0.8055197431950052 |
| descriptive.scenarios[P0/intermediate/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P0/intermediate/regional/vip0].turnover_per_hour | 171156.61138585903 | 54556.616994223186 |
| descriptive.scenarios[P0/intermediate/regional/vip0].tw_abs_inventory_avg | 5.426336611367309 | 5.539076138269047 |
| descriptive.scenarios[P0/intermediate/regional/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/intermediate/regional/vip9].fill_rate | 0.3447061432189926 | 0.30256289210734033 |
| descriptive.scenarios[P0/intermediate/regional/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P0/intermediate/regional/vip9].gross_bp_per_notional | -1.5097047231221425 | -1.4330080502894866 |
| descriptive.scenarios[P0/intermediate/regional/vip9].gross_per_hour | -26.090585369861316 | -7.701392778650965 |
| descriptive.scenarios[P0/intermediate/regional/vip9].inc_es | 10.596958333875811 | 4.839828742813028 |
| descriptive.scenarios[P0/intermediate/regional/vip9].inc_std | 2.4328821943125236 | 1.2351354183168144 |
| descriptive.scenarios[P0/intermediate/regional/vip9].inc_worst | -17.42681493693211 | -7.149385382918648 |
| descriptive.scenarios[P0/intermediate/regional/vip9].liquidation_shortfall | 0.5005999999999992 | 0.0 |
| descriptive.scenarios[P0/intermediate/regional/vip9].max_abs_inventory | 10.820099999999808 | 10.754000000000017 |
| descriptive.scenarios[P0/intermediate/regional/vip9].max_drawdown | 982.7663231106835 | 328.80403684520513 |
| descriptive.scenarios[P0/intermediate/regional/vip9].net_bp_per_notional | -2.6113842369403093 | -2.537395330009275 |
| descriptive.scenarios[P0/intermediate/regional/vip9].net_per_hour | -44.94996726136831 | -13.71934562524282 |
| descriptive.scenarios[P0/intermediate/regional/vip9].net_per_hour_over_inc_std | -16.184001867901927 | -10.352619663639281 |
| descriptive.scenarios[P0/intermediate/regional/vip9].orders_per_fill | 0.5113944690530897 | 0.8146066418163931 |
| descriptive.scenarios[P0/intermediate/regional/vip9].own_edge_bp | 0.22858500966316422 | 0.34244483305412293 |
| descriptive.scenarios[P0/intermediate/regional/vip9].own_markout_1s_bp | -1.1796616501855328 | -1.1663852891053672 |
| descriptive.scenarios[P0/intermediate/regional/vip9].own_markout_30s_bp | -1.4763560368261688 | -1.430623272880284 |
| descriptive.scenarios[P0/intermediate/regional/vip9].own_markout_5s_bp | -1.3681306937037538 | -1.3658665144869295 |
| descriptive.scenarios[P0/intermediate/regional/vip9].paced_spells | 8265.6 | 1678.2 |
| descriptive.scenarios[P0/intermediate/regional/vip9].paced_time_share | 0.02697022768744426 | 0.004917302495383665 |
| descriptive.scenarios[P0/intermediate/regional/vip9].quote_presence_ask | 0.8743528337466449 | 0.8931723502917684 |
| descriptive.scenarios[P0/intermediate/regional/vip9].quote_presence_bid | 0.8830280479877681 | 0.9053593777282364 |
| descriptive.scenarios[P0/intermediate/regional/vip9].quote_presence_both | 0.7793790708053236 | 0.8055197431950052 |
| descriptive.scenarios[P0/intermediate/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P0/intermediate/regional/vip9].turnover_per_hour | 171156.61138585903 | 54556.616994223186 |
| descriptive.scenarios[P0/intermediate/regional/vip9].tw_abs_inventory_avg | 5.426336611367309 | 5.539076138269047 |
| descriptive.scenarios[P0/intermediate/regional/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].fill_rate | 0.349580084714918 | 0.2848840195331811 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].gross_bp_per_notional | -1.683647684428239 | -1.599647653644731 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].gross_per_hour | -32.33553543499444 | -9.080399597026949 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].inc_es | 6.858326615273704 | 3.276827824106624 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].inc_std | 2.022823932426519 | 1.0274886353864476 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].inc_worst | -11.995501563839358 | -5.42025194543993 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].liquidation_shortfall | 0.5270000000000005 | 0.0 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].max_abs_inventory | 10.329400000000877 | 10.154399999999985 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].max_drawdown | 371.9599306761363 | 109.2695994753445 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].net_bp_per_notional | -0.8851368576587539 | -0.8041749822622763 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].net_per_hour | -16.81806095834868 | -4.495346858963405 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].net_per_hour_over_inc_std | -7.320967683583372 | -4.121179150856451 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].orders_per_fill | 0.47665311670165256 | 0.8142030085674467 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].own_edge_bp | 0.3596931575430407 | 0.529596838703723 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].own_markout_1s_bp | -1.3840130793457275 | -1.3379913189443795 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].own_markout_30s_bp | -1.67367958980313 | -1.5816345585276437 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].own_markout_5s_bp | -1.5720957551701493 | -1.5302672886510897 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].paced_spells | 8685.1 | 1815.2 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].paced_time_share | 0.028418782959573823 | 0.005333052419671683 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].quote_presence_ask | 0.8738289820400904 | 0.8998936770308618 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].quote_presence_bid | 0.8599639455836314 | 0.8987139113826432 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].quote_presence_both | 0.7553536560035351 | 0.8051538178219223 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].turnover_per_hour | 194392.935248968 | 57543.35347204444 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].tw_abs_inventory_avg | 5.6916616632462524 | 5.5404743277782895 |
| descriptive.scenarios[P0/intermediate/tokyo/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].fill_rate | 0.349580084714918 | 0.2848840195331811 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].gross_bp_per_notional | -1.683647684428239 | -1.599647653644731 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].gross_per_hour | -32.33553543499444 | -9.080399597026949 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].inc_es | 35.59226926016918 | 15.147605219733506 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].inc_std | 7.208152584444518 | 3.44172806138621 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].inc_worst | -45.06390862499858 | -20.952344323998528 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].liquidation_shortfall | 0.5270000000000005 | 0.0 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].max_abs_inventory | 10.329400000000877 | 10.154399999999985 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].max_drawdown | 4930.784833390759 | 1597.714026678032 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].net_bp_per_notional | -11.690122350647869 | -11.619331691112318 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].net_per_hour | -226.87612435036107 | -66.70382063298447 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].net_per_hour_over_inc_std | -28.196787275271316 | -18.06295061238747 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].orders_per_fill | 0.47665311670165256 | 0.8142030085674467 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].own_edge_bp | 0.3596931575430407 | 0.529596838703723 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].own_markout_1s_bp | -1.3840130793457275 | -1.3379913189443795 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].own_markout_30s_bp | -1.67367958980313 | -1.5816345585276437 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].own_markout_5s_bp | -1.5720957551701493 | -1.5302672886510897 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].paced_spells | 8685.1 | 1815.2 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].paced_time_share | 0.028418782959573823 | 0.005333052419671683 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].quote_presence_ask | 0.8738289820400904 | 0.8998936770308618 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].quote_presence_bid | 0.8599639455836314 | 0.8987139113826432 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].quote_presence_both | 0.7553536560035351 | 0.8051538178219223 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].turnover_per_hour | 194392.935248968 | 57543.35347204444 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].tw_abs_inventory_avg | 5.6916616632462524 | 5.5404743277782895 |
| descriptive.scenarios[P0/intermediate/tokyo/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].fill_rate | 0.349580084714918 | 0.2848840195331811 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].gross_bp_per_notional | -1.683647684428239 | -1.599647653644731 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].gross_per_hour | -32.33553543499444 | -9.080399597026949 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].inc_es | 11.312146667432314 | 5.037568547681291 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].inc_std | 2.5460925186882672 | 1.268866124712275 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].inc_worst | -16.600680975640735 | -7.385260703119502 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].liquidation_shortfall | 0.5270000000000005 | 0.0 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].max_abs_inventory | 10.329400000000877 | 10.154399999999985 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].max_drawdown | 1172.789926350322 | 369.6068752814499 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].net_bp_per_notional | -2.785136857658754 | -2.7041749822622765 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].net_per_hour | -53.7527186556526 | -15.42858401865185 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].net_per_hour_over_inc_std | -18.510526547873802 | -11.305562524017356 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].orders_per_fill | 0.47665311670165256 | 0.8142030085674467 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].own_edge_bp | 0.3596931575430407 | 0.529596838703723 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].own_markout_1s_bp | -1.3840130793457275 | -1.3379913189443795 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].own_markout_30s_bp | -1.67367958980313 | -1.5816345585276437 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].own_markout_5s_bp | -1.5720957551701493 | -1.5302672886510897 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].paced_spells | 8685.1 | 1815.2 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].paced_time_share | 0.028418782959573823 | 0.005333052419671683 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].quote_presence_ask | 0.8738289820400904 | 0.8998936770308618 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].quote_presence_bid | 0.8599639455836314 | 0.8987139113826432 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].quote_presence_both | 0.7553536560035351 | 0.8051538178219223 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].turnover_per_hour | 194392.935248968 | 57543.35347204444 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].tw_abs_inventory_avg | 5.6916616632462524 | 5.5404743277782895 |
| descriptive.scenarios[P0/intermediate/tokyo/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].fill_rate | 0.47708180036181336 | 0.49649121111536 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].gross_bp_per_notional | -1.1155874315900656 | -0.9826941350561793 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].gross_per_hour | -21.69207037004053 | -8.07720331545124 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].inc_es | 5.7218100955661475 | 2.7567999343466743 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].inc_std | 1.9201345213124363 | 0.9446565912637379 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].inc_worst | -12.981229264678955 | -4.775215343199562 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].liquidation_shortfall | 0.4706999999999999 | 0.0 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].max_abs_inventory | 10.515199999999961 | 9.998600000000046 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].max_drawdown | 158.28958885308487 | 45.735682805539376 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].net_bp_per_notional | -0.31692090235714626 | -0.1849597613648738 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].net_per_hour | -6.8027429659985685 | -1.555081758774306 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].net_per_hour_over_inc_std | -2.8674519713536393 | -1.5511919431119647 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].orders_per_fill | 0.5455887060452671 | 0.7254367517150577 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].own_edge_bp | 0.41730804091070983 | 0.58020707924803 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].own_markout_1s_bp | -0.7818640946383739 | -0.72786394829674 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].own_markout_30s_bp | -1.0791269355290187 | -0.996439327963721 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].own_markout_5s_bp | -0.9754250122655114 | -0.934525540532323 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].paced_spells | 9688.2 | 2379.0 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].paced_time_share | 0.03130217634131174 | 0.006995925645094476 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].quote_presence_ask | 0.819586785435194 | 0.8777091148189285 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].quote_presence_bid | 0.8573762450975705 | 0.8767012860933983 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].quote_presence_both | 0.7099144909022717 | 0.7662979812905195 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].turnover_per_hour | 186479.13127186758 | 81717.26713571126 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].tw_abs_inventory_avg | 5.410294650791167 | 5.435717613705192 |
| descriptive.scenarios[P0/optimistic/distant/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/optimistic/distant/vip0].fill_rate | 0.47708180036181336 | 0.49649121111536 |
| descriptive.scenarios[P0/optimistic/distant/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P0/optimistic/distant/vip0].gross_bp_per_notional | -1.1155874315900656 | -0.9826941350561793 |
| descriptive.scenarios[P0/optimistic/distant/vip0].gross_per_hour | -21.69207037004053 | -8.07720331545124 |
| descriptive.scenarios[P0/optimistic/distant/vip0].inc_es | 30.04481284936652 | 18.024371557733 |
| descriptive.scenarios[P0/optimistic/distant/vip0].inc_std | 5.6912243606554345 | 3.8892392793180703 |
| descriptive.scenarios[P0/optimistic/distant/vip0].inc_worst | -36.482507345000805 | -22.188296084001603 |
| descriptive.scenarios[P0/optimistic/distant/vip0].liquidation_shortfall | 0.4706999999999999 | 0.0 |
| descriptive.scenarios[P0/optimistic/distant/vip0].max_abs_inventory | 10.515199999999961 | 9.998600000000046 |
| descriptive.scenarios[P0/optimistic/distant/vip0].max_drawdown | 4576.166794600901 | 2151.61841262195 |
| descriptive.scenarios[P0/optimistic/distant/vip0].net_bp_per_notional | -11.121385130577373 | -10.992544684224416 |
| descriptive.scenarios[P0/optimistic/distant/vip0].net_per_hour | -208.29730206672312 | -89.86081746933627 |
| descriptive.scenarios[P0/optimistic/distant/vip0].net_per_hour_over_inc_std | -33.46752453006611 | -21.839520719519506 |
| descriptive.scenarios[P0/optimistic/distant/vip0].orders_per_fill | 0.5455887060452671 | 0.7254367517150577 |
| descriptive.scenarios[P0/optimistic/distant/vip0].own_edge_bp | 0.41730804091070983 | 0.58020707924803 |
| descriptive.scenarios[P0/optimistic/distant/vip0].own_markout_1s_bp | -0.7818640946383739 | -0.72786394829674 |
| descriptive.scenarios[P0/optimistic/distant/vip0].own_markout_30s_bp | -1.0791269355290187 | -0.996439327963721 |
| descriptive.scenarios[P0/optimistic/distant/vip0].own_markout_5s_bp | -0.9754250122655114 | -0.934525540532323 |
| descriptive.scenarios[P0/optimistic/distant/vip0].paced_spells | 9688.2 | 2379.0 |
| descriptive.scenarios[P0/optimistic/distant/vip0].paced_time_share | 0.03130217634131174 | 0.006995925645094476 |
| descriptive.scenarios[P0/optimistic/distant/vip0].quote_presence_ask | 0.819586785435194 | 0.8777091148189285 |
| descriptive.scenarios[P0/optimistic/distant/vip0].quote_presence_bid | 0.8573762450975705 | 0.8767012860933983 |
| descriptive.scenarios[P0/optimistic/distant/vip0].quote_presence_both | 0.7099144909022717 | 0.7662979812905195 |
| descriptive.scenarios[P0/optimistic/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P0/optimistic/distant/vip0].turnover_per_hour | 186479.13127186758 | 81717.26713571126 |
| descriptive.scenarios[P0/optimistic/distant/vip0].tw_abs_inventory_avg | 5.410294650791167 | 5.435717613705192 |
| descriptive.scenarios[P0/optimistic/distant/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/optimistic/distant/vip9].fill_rate | 0.47708180036181336 | 0.49649121111536 |
| descriptive.scenarios[P0/optimistic/distant/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P0/optimistic/distant/vip9].gross_bp_per_notional | -1.1155874315900656 | -0.9826941350561793 |
| descriptive.scenarios[P0/optimistic/distant/vip9].gross_per_hour | -21.69207037004053 | -8.07720331545124 |
| descriptive.scenarios[P0/optimistic/distant/vip9].inc_es | 9.467377365841944 | 4.923251367147822 |
| descriptive.scenarios[P0/optimistic/distant/vip9].inc_std | 2.178332040196218 | 1.2183796650777639 |
| descriptive.scenarios[P0/optimistic/distant/vip9].inc_worst | -16.717473032828785 | -7.126800104399521 |
| descriptive.scenarios[P0/optimistic/distant/vip9].liquidation_shortfall | 0.4706999999999999 | 0.0 |
| descriptive.scenarios[P0/optimistic/distant/vip9].max_abs_inventory | 10.515199999999961 | 9.998600000000046 |
| descriptive.scenarios[P0/optimistic/distant/vip9].max_drawdown | 929.8824306647573 | 409.15140546273494 |
| descriptive.scenarios[P0/optimistic/distant/vip9].net_bp_per_notional | -2.2169209023571463 | -2.084959761364874 |
| descriptive.scenarios[P0/optimistic/distant/vip9].net_per_hour | -42.23377790765341 | -17.081362514559448 |
| descriptive.scenarios[P0/optimistic/distant/vip9].net_per_hour_over_inc_std | -17.49681653677844 | -13.129070749312808 |
| descriptive.scenarios[P0/optimistic/distant/vip9].orders_per_fill | 0.5455887060452671 | 0.7254367517150577 |
| descriptive.scenarios[P0/optimistic/distant/vip9].own_edge_bp | 0.41730804091070983 | 0.58020707924803 |
| descriptive.scenarios[P0/optimistic/distant/vip9].own_markout_1s_bp | -0.7818640946383739 | -0.72786394829674 |
| descriptive.scenarios[P0/optimistic/distant/vip9].own_markout_30s_bp | -1.0791269355290187 | -0.996439327963721 |
| descriptive.scenarios[P0/optimistic/distant/vip9].own_markout_5s_bp | -0.9754250122655114 | -0.934525540532323 |
| descriptive.scenarios[P0/optimistic/distant/vip9].paced_spells | 9688.2 | 2379.0 |
| descriptive.scenarios[P0/optimistic/distant/vip9].paced_time_share | 0.03130217634131174 | 0.006995925645094476 |
| descriptive.scenarios[P0/optimistic/distant/vip9].quote_presence_ask | 0.819586785435194 | 0.8777091148189285 |
| descriptive.scenarios[P0/optimistic/distant/vip9].quote_presence_bid | 0.8573762450975705 | 0.8767012860933983 |
| descriptive.scenarios[P0/optimistic/distant/vip9].quote_presence_both | 0.7099144909022717 | 0.7662979812905195 |
| descriptive.scenarios[P0/optimistic/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P0/optimistic/distant/vip9].turnover_per_hour | 186479.13127186758 | 81717.26713571126 |
| descriptive.scenarios[P0/optimistic/distant/vip9].tw_abs_inventory_avg | 5.410294650791167 | 5.435717613705192 |
| descriptive.scenarios[P0/optimistic/distant/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].fill_rate | 0.5731911382995388 | 0.5758097353288768 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].gross_bp_per_notional | -1.1877920741592187 | -1.0660452759633867 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].gross_per_hour | -34.693225412201386 | -12.207125693118297 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].inc_es | 6.495048220182696 | 3.066922209770686 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].inc_std | 2.0076664170730334 | 0.9967210858313683 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].inc_worst | -12.763861612962454 | -5.607239037598797 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].liquidation_shortfall | 0.49869999999999753 | 0.0 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].max_abs_inventory | 10.374100000000297 | 10.101800000000036 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].max_drawdown | 269.17735055021956 | 82.91162370244385 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].net_bp_per_notional | -0.38881728138719784 | -0.2681945513837668 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].net_per_hour | -12.13101037843489 | -3.1851974219524237 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].net_per_hour_over_inc_std | -5.064336741416995 | -2.952430000909633 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].orders_per_fill | 0.47247469091931266 | 0.6462385003026053 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].own_edge_bp | 0.4121131625741494 | 0.5775235450960421 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].own_markout_1s_bp | -0.8703509264544762 | -0.8210300730939478 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].own_markout_30s_bp | -1.15656342729148 | -1.068052682442539 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].own_markout_5s_bp | -1.0573404809665579 | -1.0200767599382865 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].paced_spells | 12470.6 | 3103.2 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].paced_time_share | 0.04048046435366665 | 0.00916191508410794 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].quote_presence_ask | 0.8372388025772788 | 0.8916090340852565 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].quote_presence_bid | 0.8664736458752287 | 0.8889481695408925 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].quote_presence_both | 0.7345721480353373 | 0.7902982030916842 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].turnover_per_hour | 282445.4498469428 | 112981.54434763291 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].tw_abs_inventory_avg | 5.387159220319179 | 5.396513483568827 |
| descriptive.scenarios[P0/optimistic/regional/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/optimistic/regional/vip0].fill_rate | 0.5731911382995388 | 0.5758097353288768 |
| descriptive.scenarios[P0/optimistic/regional/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P0/optimistic/regional/vip0].gross_bp_per_notional | -1.1877920741592187 | -1.0660452759633867 |
| descriptive.scenarios[P0/optimistic/regional/vip0].gross_per_hour | -34.693225412201386 | -12.207125693118297 |
| descriptive.scenarios[P0/optimistic/regional/vip0].inc_es | 45.10299835911817 | 25.755863307332127 |
| descriptive.scenarios[P0/optimistic/regional/vip0].inc_std | 8.513037477854734 | 5.652752165041886 |
| descriptive.scenarios[P0/optimistic/regional/vip0].inc_worst | -54.915754038990414 | -31.819956469997656 |
| descriptive.scenarios[P0/optimistic/regional/vip0].liquidation_shortfall | 0.49869999999999753 | 0.0 |
| descriptive.scenarios[P0/optimistic/regional/vip0].max_abs_inventory | 10.374100000000297 | 10.101800000000036 |
| descriptive.scenarios[P0/optimistic/regional/vip0].max_drawdown | 6940.987009910888 | 2999.232859891895 |
| descriptive.scenarios[P0/optimistic/regional/vip0].net_bp_per_notional | -11.192249496889563 | -11.075389951704171 |
| descriptive.scenarios[P0/optimistic/regional/vip0].net_per_hour | -317.2839837547482 | -125.26082341746758 |
| descriptive.scenarios[P0/optimistic/regional/vip0].net_per_hour_over_inc_std | -33.961980373329546 | -20.870278615626802 |
| descriptive.scenarios[P0/optimistic/regional/vip0].orders_per_fill | 0.47247469091931266 | 0.6462385003026053 |
| descriptive.scenarios[P0/optimistic/regional/vip0].own_edge_bp | 0.4121131625741494 | 0.5775235450960421 |
| descriptive.scenarios[P0/optimistic/regional/vip0].own_markout_1s_bp | -0.8703509264544762 | -0.8210300730939478 |
| descriptive.scenarios[P0/optimistic/regional/vip0].own_markout_30s_bp | -1.15656342729148 | -1.068052682442539 |
| descriptive.scenarios[P0/optimistic/regional/vip0].own_markout_5s_bp | -1.0573404809665579 | -1.0200767599382865 |
| descriptive.scenarios[P0/optimistic/regional/vip0].paced_spells | 12470.6 | 3103.2 |
| descriptive.scenarios[P0/optimistic/regional/vip0].paced_time_share | 0.04048046435366665 | 0.00916191508410794 |
| descriptive.scenarios[P0/optimistic/regional/vip0].quote_presence_ask | 0.8372388025772788 | 0.8916090340852565 |
| descriptive.scenarios[P0/optimistic/regional/vip0].quote_presence_bid | 0.8664736458752287 | 0.8889481695408925 |
| descriptive.scenarios[P0/optimistic/regional/vip0].quote_presence_both | 0.7345721480353373 | 0.7902982030916842 |
| descriptive.scenarios[P0/optimistic/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P0/optimistic/regional/vip0].turnover_per_hour | 282445.4498469428 | 112981.54434763291 |
| descriptive.scenarios[P0/optimistic/regional/vip0].tw_abs_inventory_avg | 5.387159220319179 | 5.396513483568827 |
| descriptive.scenarios[P0/optimistic/regional/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/optimistic/regional/vip9].fill_rate | 0.5731911382995388 | 0.5758097353288768 |
| descriptive.scenarios[P0/optimistic/regional/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P0/optimistic/regional/vip9].gross_bp_per_notional | -1.1877920741592187 | -1.0660452759633867 |
| descriptive.scenarios[P0/optimistic/regional/vip9].gross_per_hour | -34.693225412201386 | -12.207125693118297 |
| descriptive.scenarios[P0/optimistic/regional/vip9].inc_es | 12.551806675197374 | 6.497188901955724 |
| descriptive.scenarios[P0/optimistic/regional/vip9].inc_std | 2.6459633689668047 | 1.5439721161315163 |
| descriptive.scenarios[P0/optimistic/regional/vip9].inc_worst | -19.723787705141525 | -9.252957588558203 |
| descriptive.scenarios[P0/optimistic/regional/vip9].liquidation_shortfall | 0.49869999999999753 | 0.0 |
| descriptive.scenarios[P0/optimistic/regional/vip9].max_abs_inventory | 10.374100000000297 | 10.101800000000036 |
| descriptive.scenarios[P0/optimistic/regional/vip9].max_drawdown | 1440.2776017029632 | 590.2920759038474 |
| descriptive.scenarios[P0/optimistic/regional/vip9].net_bp_per_notional | -2.288817281387198 | -2.168194551383767 |
| descriptive.scenarios[P0/optimistic/regional/vip9].net_per_hour | -65.79564584935403 | -24.65169084800268 |
| descriptive.scenarios[P0/optimistic/regional/vip9].net_per_hour_over_inc_std | -22.141321735606212 | -14.871519943164 |
| descriptive.scenarios[P0/optimistic/regional/vip9].orders_per_fill | 0.47247469091931266 | 0.6462385003026053 |
| descriptive.scenarios[P0/optimistic/regional/vip9].own_edge_bp | 0.4121131625741494 | 0.5775235450960421 |
| descriptive.scenarios[P0/optimistic/regional/vip9].own_markout_1s_bp | -0.8703509264544762 | -0.8210300730939478 |
| descriptive.scenarios[P0/optimistic/regional/vip9].own_markout_30s_bp | -1.15656342729148 | -1.068052682442539 |
| descriptive.scenarios[P0/optimistic/regional/vip9].own_markout_5s_bp | -1.0573404809665579 | -1.0200767599382865 |
| descriptive.scenarios[P0/optimistic/regional/vip9].paced_spells | 12470.6 | 3103.2 |
| descriptive.scenarios[P0/optimistic/regional/vip9].paced_time_share | 0.04048046435366665 | 0.00916191508410794 |
| descriptive.scenarios[P0/optimistic/regional/vip9].quote_presence_ask | 0.8372388025772788 | 0.8916090340852565 |
| descriptive.scenarios[P0/optimistic/regional/vip9].quote_presence_bid | 0.8664736458752287 | 0.8889481695408925 |
| descriptive.scenarios[P0/optimistic/regional/vip9].quote_presence_both | 0.7345721480353373 | 0.7902982030916842 |
| descriptive.scenarios[P0/optimistic/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P0/optimistic/regional/vip9].turnover_per_hour | 282445.4498469428 | 112981.54434763291 |
| descriptive.scenarios[P0/optimistic/regional/vip9].tw_abs_inventory_avg | 5.387159220319179 | 5.396513483568827 |
| descriptive.scenarios[P0/optimistic/regional/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].fill_rate | 0.6192939616950055 | 0.6212136092577694 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].gross_bp_per_notional | -1.375612263484926 | -1.2584853119672768 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].gross_per_hour | -48.30608316390596 | -17.580109550100836 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].inc_es | 7.193792852189917 | 3.600489951648202 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].inc_std | 2.0661747335335345 | 1.0897166244976206 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].inc_worst | -13.007751894640538 | -5.968184922720221 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].liquidation_shortfall | 0.46799999999999586 | 0.0 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].max_abs_inventory | 10.026000000000016 | 10.000000000000007 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].max_drawdown | 452.53450981469194 | 159.4193891463517 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].net_bp_per_notional | -0.5764767189623525 | -0.4602007075296145 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].net_per_hour | -20.562474859545677 | -6.509623792064465 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].net_per_hour_over_inc_std | -8.74690311363711 | -5.528995683450077 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].orders_per_fill | 0.3784308099465273 | 0.5175438025639467 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].own_edge_bp | 0.4111982354984831 | 0.577103522634536 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].own_markout_1s_bp | -1.0608261376188897 | -1.0021909471448036 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].own_markout_30s_bp | -1.3469516685182414 | -1.234988322000801 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].own_markout_5s_bp | -1.249204476661783 | -1.1954941605195002 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].paced_spells | 11363.7 | 2619.0 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].paced_time_share | 0.03655055411433538 | 0.007628925517931344 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].quote_presence_ask | 0.8492271168478502 | 0.8923450643363555 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].quote_presence_bid | 0.861221277819294 | 0.8924372388409738 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].quote_presence_both | 0.7366546176883435 | 0.7925254349062524 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].turnover_per_hour | 347221.11379047006 | 138593.34635375426 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].tw_abs_inventory_avg | 5.527613663438666 | 5.404682570311978 |
| descriptive.scenarios[P0/optimistic/tokyo/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].fill_rate | 0.6192939616950055 | 0.6212136092577694 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].gross_bp_per_notional | -1.375612263484926 | -1.2584853119672768 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].gross_per_hour | -48.30608316390596 | -17.580109550100836 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].inc_es | 53.4433024644958 | 31.547080214266305 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].inc_std | 10.35310925755066 | 7.012098296688485 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].inc_worst | -62.22497395200111 | -38.347475429999804 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].liquidation_shortfall | 0.46799999999999586 | 0.0 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].max_abs_inventory | 10.026000000000016 | 10.000000000000007 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].max_drawdown | 8660.309455898781 | 3741.498631495858 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].net_bp_per_notional | -11.379370765560694 | -11.265943553542659 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].net_per_hour | -395.6753743407992 | -156.2472904702202 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].net_per_hour_over_inc_std | -35.0162258263738 | -20.972569576398456 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].orders_per_fill | 0.3784308099465273 | 0.5175438025639467 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].own_edge_bp | 0.4111982354984831 | 0.577103522634536 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].own_markout_1s_bp | -1.0608261376188897 | -1.0021909471448036 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].own_markout_30s_bp | -1.3469516685182414 | -1.234988322000801 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].own_markout_5s_bp | -1.249204476661783 | -1.1954941605195002 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].paced_spells | 11363.7 | 2619.0 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].paced_time_share | 0.03655055411433538 | 0.007628925517931344 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].quote_presence_ask | 0.8492271168478502 | 0.8923450643363555 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].quote_presence_bid | 0.861221277819294 | 0.8924372388409738 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].quote_presence_both | 0.7366546176883435 | 0.7925254349062524 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].turnover_per_hour | 347221.11379047006 | 138593.34635375426 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].tw_abs_inventory_avg | 5.527613663438666 | 5.404682570311978 |
| descriptive.scenarios[P0/optimistic/tokyo/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].fill_rate | 0.6192939616950055 | 0.6212136092577694 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].gross_bp_per_notional | -1.375612263484926 | -1.2584853119672768 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].gross_per_hour | -48.30608316390596 | -17.580109550100836 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].inc_es | 14.517344436159481 | 7.992283721475855 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].inc_std | 2.9975544536197902 | 1.8668877114522182 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].inc_worst | -20.712969801949463 | -10.550989436819608 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].liquidation_shortfall | 0.46799999999999586 | 0.0 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].max_abs_inventory | 10.026000000000016 | 10.000000000000007 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].max_drawdown | 1895.4381077573757 | 786.4398441035074 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].net_bp_per_notional | -2.4764767189623527 | -2.3602007075296147 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].net_per_hour | -86.534486479735 | -32.84235959927778 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].net_per_hour_over_inc_std | -25.768077654907994 | -16.412543376651833 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].orders_per_fill | 0.3784308099465273 | 0.5175438025639467 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].own_edge_bp | 0.4111982354984831 | 0.577103522634536 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].own_markout_1s_bp | -1.0608261376188897 | -1.0021909471448036 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].own_markout_30s_bp | -1.3469516685182414 | -1.234988322000801 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].own_markout_5s_bp | -1.249204476661783 | -1.1954941605195002 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].paced_spells | 11363.7 | 2619.0 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].paced_time_share | 0.03655055411433538 | 0.007628925517931344 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].quote_presence_ask | 0.8492271168478502 | 0.8923450643363555 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].quote_presence_bid | 0.861221277819294 | 0.8924372388409738 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].quote_presence_both | 0.7366546176883435 | 0.7925254349062524 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].turnover_per_hour | 347221.11379047006 | 138593.34635375426 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].tw_abs_inventory_avg | 5.527613663438666 | 5.404682570311978 |
| descriptive.scenarios[P0/optimistic/tokyo/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].fill_rate | 0.2739486354229751 | 0.24208443900053603 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].gross_bp_per_notional | -1.6502834383347165 | -1.64331837584364 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].gross_per_hour | -17.367640980485834 | -5.632526187587064 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].inc_es | 3.07589641428748 | 1.4339606373012956 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].inc_std | 0.8357754724929464 | 0.41686570592010985 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].inc_worst | -5.394185476321448 | -2.6203636161599744 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].max_abs_inventory | 4.836699999999843 | 4.844400000000011 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].max_drawdown | 201.30512724975665 | 69.13244435463727 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].net_bp_per_notional | -0.8515547988079855 | -0.8468616060297623 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].net_per_hour | -9.109496016310732 | -2.8750981762003414 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].net_per_hour_over_inc_std | -9.310192313186175 | -6.39464908919747 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].orders_per_fill | 0.568973903433553 | 0.8507291146459636 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].own_edge_bp | 0.1970594099951913 | 0.2158515371124634 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].own_markout_1s_bp | -1.3308013279138902 | -1.4052534491498727 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].own_markout_30s_bp | -1.637279193327362 | -1.6564568149070809 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].own_markout_5s_bp | -1.5251770464445467 | -1.6029035343387854 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].paced_spells | 5417.7 | 1041.2 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].paced_time_share | 0.017679893839080377 | 0.003083477918772723 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].quote_presence_ask | 0.7979073936225567 | 0.811088255740019 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].quote_presence_bid | 0.8004792563350469 | 0.8490225510546813 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].quote_presence_both | 0.6239349339097497 | 0.6690690317876944 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].turnover_per_hour | 103388.51614896517 | 34568.60632142106 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].tw_abs_inventory_avg | 2.111047055252372 | 2.087686652098924 |
| descriptive.scenarios[P1/conservative/distant/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/conservative/distant/vip0].fill_rate | 0.2739486354229751 | 0.24208443900053603 |
| descriptive.scenarios[P1/conservative/distant/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P1/conservative/distant/vip0].gross_bp_per_notional | -1.6502834383347165 | -1.64331837584364 |
| descriptive.scenarios[P1/conservative/distant/vip0].gross_per_hour | -17.367640980485834 | -5.632526187587064 |
| descriptive.scenarios[P1/conservative/distant/vip0].inc_es | 20.52396562678293 | 10.158280911199913 |
| descriptive.scenarios[P1/conservative/distant/vip0].inc_std | 4.379182570962287 | 2.2834193116528096 |
| descriptive.scenarios[P1/conservative/distant/vip0].inc_worst | -25.135079654999394 | -14.201801603999604 |
| descriptive.scenarios[P1/conservative/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/conservative/distant/vip0].max_abs_inventory | 4.836699999999843 | 4.844400000000011 |
| descriptive.scenarios[P1/conservative/distant/vip0].max_drawdown | 2643.195620506854 | 963.7160170500114 |
| descriptive.scenarios[P1/conservative/distant/vip0].net_bp_per_notional | -11.65581109256632 | -11.658723724478955 |
| descriptive.scenarios[P1/conservative/distant/vip0].net_per_hour | -120.8124020326776 | -40.23617813651666 |
| descriptive.scenarios[P1/conservative/distant/vip0].net_per_hour_over_inc_std | -24.509916797278017 | -16.39476579615029 |
| descriptive.scenarios[P1/conservative/distant/vip0].orders_per_fill | 0.568973903433553 | 0.8507291146459636 |
| descriptive.scenarios[P1/conservative/distant/vip0].own_edge_bp | 0.1970594099951913 | 0.2158515371124634 |
| descriptive.scenarios[P1/conservative/distant/vip0].own_markout_1s_bp | -1.3308013279138902 | -1.4052534491498727 |
| descriptive.scenarios[P1/conservative/distant/vip0].own_markout_30s_bp | -1.637279193327362 | -1.6564568149070809 |
| descriptive.scenarios[P1/conservative/distant/vip0].own_markout_5s_bp | -1.5251770464445467 | -1.6029035343387854 |
| descriptive.scenarios[P1/conservative/distant/vip0].paced_spells | 5417.7 | 1041.2 |
| descriptive.scenarios[P1/conservative/distant/vip0].paced_time_share | 0.017679893839080377 | 0.003083477918772723 |
| descriptive.scenarios[P1/conservative/distant/vip0].quote_presence_ask | 0.7979073936225567 | 0.811088255740019 |
| descriptive.scenarios[P1/conservative/distant/vip0].quote_presence_bid | 0.8004792563350469 | 0.8490225510546813 |
| descriptive.scenarios[P1/conservative/distant/vip0].quote_presence_both | 0.6239349339097497 | 0.6690690317876944 |
| descriptive.scenarios[P1/conservative/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P1/conservative/distant/vip0].turnover_per_hour | 103388.51614896517 | 34568.60632142106 |
| descriptive.scenarios[P1/conservative/distant/vip0].tw_abs_inventory_avg | 2.111047055252372 | 2.087686652098924 |
| descriptive.scenarios[P1/conservative/distant/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/conservative/distant/vip9].fill_rate | 0.2739486354229751 | 0.24208443900053603 |
| descriptive.scenarios[P1/conservative/distant/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P1/conservative/distant/vip9].gross_bp_per_notional | -1.6502834383347165 | -1.64331837584364 |
| descriptive.scenarios[P1/conservative/distant/vip9].gross_per_hour | -17.367640980485834 | -5.632526187587064 |
| descriptive.scenarios[P1/conservative/distant/vip9].inc_es | 5.765013340747342 | 2.7770829141545947 |
| descriptive.scenarios[P1/conservative/distant/vip9].inc_std | 1.2796486687800281 | 0.6657205662912039 |
| descriptive.scenarios[P1/conservative/distant/vip9].inc_worst | -8.392755929149704 | -4.36675730673961 |
| descriptive.scenarios[P1/conservative/distant/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/conservative/distant/vip9].max_abs_inventory | 4.836699999999843 | 4.844400000000011 |
| descriptive.scenarios[P1/conservative/distant/vip9].max_drawdown | 630.5688144259636 | 226.15922023167977 |
| descriptive.scenarios[P1/conservative/distant/vip9].net_bp_per_notional | -2.7515547988079856 | -2.7468616060297624 |
| descriptive.scenarios[P1/conservative/distant/vip9].net_per_hour | -28.75331408461411 | -9.443133377270344 |
| descriptive.scenarios[P1/conservative/distant/vip9].net_per_hour_over_inc_std | -19.57242444470224 | -13.10723599321027 |
| descriptive.scenarios[P1/conservative/distant/vip9].orders_per_fill | 0.568973903433553 | 0.8507291146459636 |
| descriptive.scenarios[P1/conservative/distant/vip9].own_edge_bp | 0.1970594099951913 | 0.2158515371124634 |
| descriptive.scenarios[P1/conservative/distant/vip9].own_markout_1s_bp | -1.3308013279138902 | -1.4052534491498727 |
| descriptive.scenarios[P1/conservative/distant/vip9].own_markout_30s_bp | -1.637279193327362 | -1.6564568149070809 |
| descriptive.scenarios[P1/conservative/distant/vip9].own_markout_5s_bp | -1.5251770464445467 | -1.6029035343387854 |
| descriptive.scenarios[P1/conservative/distant/vip9].paced_spells | 5417.7 | 1041.2 |
| descriptive.scenarios[P1/conservative/distant/vip9].paced_time_share | 0.017679893839080377 | 0.003083477918772723 |
| descriptive.scenarios[P1/conservative/distant/vip9].quote_presence_ask | 0.7979073936225567 | 0.811088255740019 |
| descriptive.scenarios[P1/conservative/distant/vip9].quote_presence_bid | 0.8004792563350469 | 0.8490225510546813 |
| descriptive.scenarios[P1/conservative/distant/vip9].quote_presence_both | 0.6239349339097497 | 0.6690690317876944 |
| descriptive.scenarios[P1/conservative/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P1/conservative/distant/vip9].turnover_per_hour | 103388.51614896517 | 34568.60632142106 |
| descriptive.scenarios[P1/conservative/distant/vip9].tw_abs_inventory_avg | 2.111047055252372 | 2.087686652098924 |
| descriptive.scenarios[P1/conservative/distant/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].fill_rate | 0.27351096298107436 | 0.22842837597246538 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].gross_bp_per_notional | -1.6679395269471666 | -1.6747213208444314 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].gross_per_hour | -20.85966735515414 | -6.045146880348414 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].inc_es | 3.3813626111787563 | 1.5973841681279488 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].inc_std | 0.9055645765588369 | 0.45969443980829483 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].inc_worst | -5.738086414481005 | -2.7658765926398914 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].max_abs_inventory | 4.853099999999726 | 4.823199999999981 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].max_drawdown | 239.75590900136095 | 75.17642380797625 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].net_bp_per_notional | -0.8690044905585405 | -0.8780355731104796 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].net_per_hour | -10.912053703005533 | -3.128973139737111 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].net_per_hour_over_inc_std | -10.326490195061265 | -6.325638044056723 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].orders_per_fill | 0.5207861367318474 | 0.848678027990354 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].own_edge_bp | 0.17531511946742775 | 0.2513045897545026 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].own_markout_1s_bp | -1.3856038442718352 | -1.4237354580097956 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].own_markout_30s_bp | -1.6559289277810976 | -1.6891831522438374 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].own_markout_5s_bp | -1.568119643691203 | -1.6214742991987827 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].paced_spells | 5687.6 | 1022.4 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].paced_time_share | 0.018678662968384975 | 0.0029824127826410486 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].quote_presence_ask | 0.8035303236110737 | 0.8089629014414796 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].quote_presence_bid | 0.801168248651749 | 0.845037423088834 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].quote_presence_both | 0.6239639031960096 | 0.6601160726914811 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].turnover_per_hour | 124509.91473808789 | 36550.83289980296 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].tw_abs_inventory_avg | 2.1567657793845902 | 2.129350247368783 |
| descriptive.scenarios[P1/conservative/regional/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/conservative/regional/vip0].fill_rate | 0.27351096298107436 | 0.22842837597246538 |
| descriptive.scenarios[P1/conservative/regional/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P1/conservative/regional/vip0].gross_bp_per_notional | -1.6679395269471666 | -1.6747213208444314 |
| descriptive.scenarios[P1/conservative/regional/vip0].gross_per_hour | -20.85966735515414 | -6.045146880348414 |
| descriptive.scenarios[P1/conservative/regional/vip0].inc_es | 26.74572381477065 | 11.180396143599998 |
| descriptive.scenarios[P1/conservative/regional/vip0].inc_std | 5.736401732813581 | 2.5482809324481868 |
| descriptive.scenarios[P1/conservative/regional/vip0].inc_worst | -34.816498605990716 | -16.786748423999736 |
| descriptive.scenarios[P1/conservative/regional/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/conservative/regional/vip0].max_abs_inventory | 4.853099999999726 | 4.823199999999981 |
| descriptive.scenarios[P1/conservative/regional/vip0].max_drawdown | 3169.9075337458116 | 1021.1396669720203 |
| descriptive.scenarios[P1/conservative/regional/vip0].net_bp_per_notional | -11.672569803518359 | -11.68913111330551 |
| descriptive.scenarios[P1/conservative/regional/vip0].net_per_hour | -145.42688438410477 | -42.630296699164134 |
| descriptive.scenarios[P1/conservative/regional/vip0].net_per_hour_over_inc_std | -22.527000630641204 | -15.514985963597198 |
| descriptive.scenarios[P1/conservative/regional/vip0].orders_per_fill | 0.5207861367318474 | 0.848678027990354 |
| descriptive.scenarios[P1/conservative/regional/vip0].own_edge_bp | 0.17531511946742775 | 0.2513045897545026 |
| descriptive.scenarios[P1/conservative/regional/vip0].own_markout_1s_bp | -1.3856038442718352 | -1.4237354580097956 |
| descriptive.scenarios[P1/conservative/regional/vip0].own_markout_30s_bp | -1.6559289277810976 | -1.6891831522438374 |
| descriptive.scenarios[P1/conservative/regional/vip0].own_markout_5s_bp | -1.568119643691203 | -1.6214742991987827 |
| descriptive.scenarios[P1/conservative/regional/vip0].paced_spells | 5687.6 | 1022.4 |
| descriptive.scenarios[P1/conservative/regional/vip0].paced_time_share | 0.018678662968384975 | 0.0029824127826410486 |
| descriptive.scenarios[P1/conservative/regional/vip0].quote_presence_ask | 0.8035303236110737 | 0.8089629014414796 |
| descriptive.scenarios[P1/conservative/regional/vip0].quote_presence_bid | 0.801168248651749 | 0.845037423088834 |
| descriptive.scenarios[P1/conservative/regional/vip0].quote_presence_both | 0.6239639031960096 | 0.6601160726914811 |
| descriptive.scenarios[P1/conservative/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P1/conservative/regional/vip0].turnover_per_hour | 124509.91473808789 | 36550.83289980296 |
| descriptive.scenarios[P1/conservative/regional/vip0].tw_abs_inventory_avg | 2.1567657793845902 | 2.129350247368783 |
| descriptive.scenarios[P1/conservative/regional/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/conservative/regional/vip9].fill_rate | 0.27351096298107436 | 0.22842837597246538 |
| descriptive.scenarios[P1/conservative/regional/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P1/conservative/regional/vip9].gross_bp_per_notional | -1.6679395269471666 | -1.6747213208444314 |
| descriptive.scenarios[P1/conservative/regional/vip9].gross_per_hour | -20.85966735515414 | -6.045146880348414 |
| descriptive.scenarios[P1/conservative/regional/vip9].inc_es | 7.125389571278826 | 3.1176855048826595 |
| descriptive.scenarios[P1/conservative/regional/vip9].inc_std | 1.5842495077022432 | 0.7467513729014017 |
| descriptive.scenarios[P1/conservative/regional/vip9].inc_worst | -10.366541965180208 | -4.8969250103197925 |
| descriptive.scenarios[P1/conservative/regional/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/conservative/regional/vip9].max_abs_inventory | 4.853099999999726 | 4.823199999999981 |
| descriptive.scenarios[P1/conservative/regional/vip9].max_drawdown | 754.9142882613129 | 241.2777732527406 |
| descriptive.scenarios[P1/conservative/regional/vip9].net_bp_per_notional | -2.769004490558541 | -2.7780355731104796 |
| descriptive.scenarios[P1/conservative/regional/vip9].net_per_hour | -34.56893750324223 | -10.073631390699672 |
| descriptive.scenarios[P1/conservative/regional/vip9].net_per_hour_over_inc_std | -19.054474573014936 | -12.468542940508762 |
| descriptive.scenarios[P1/conservative/regional/vip9].orders_per_fill | 0.5207861367318474 | 0.848678027990354 |
| descriptive.scenarios[P1/conservative/regional/vip9].own_edge_bp | 0.17531511946742775 | 0.2513045897545026 |
| descriptive.scenarios[P1/conservative/regional/vip9].own_markout_1s_bp | -1.3856038442718352 | -1.4237354580097956 |
| descriptive.scenarios[P1/conservative/regional/vip9].own_markout_30s_bp | -1.6559289277810976 | -1.6891831522438374 |
| descriptive.scenarios[P1/conservative/regional/vip9].own_markout_5s_bp | -1.568119643691203 | -1.6214742991987827 |
| descriptive.scenarios[P1/conservative/regional/vip9].paced_spells | 5687.6 | 1022.4 |
| descriptive.scenarios[P1/conservative/regional/vip9].paced_time_share | 0.018678662968384975 | 0.0029824127826410486 |
| descriptive.scenarios[P1/conservative/regional/vip9].quote_presence_ask | 0.8035303236110737 | 0.8089629014414796 |
| descriptive.scenarios[P1/conservative/regional/vip9].quote_presence_bid | 0.801168248651749 | 0.845037423088834 |
| descriptive.scenarios[P1/conservative/regional/vip9].quote_presence_both | 0.6239639031960096 | 0.6601160726914811 |
| descriptive.scenarios[P1/conservative/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P1/conservative/regional/vip9].turnover_per_hour | 124509.91473808789 | 36550.83289980296 |
| descriptive.scenarios[P1/conservative/regional/vip9].tw_abs_inventory_avg | 2.1567657793845902 | 2.129350247368783 |
| descriptive.scenarios[P1/conservative/regional/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].fill_rate | 0.2724341681342205 | 0.20721984592367065 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].gross_bp_per_notional | -1.810518700750368 | -1.8106715989945201 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].gross_per_hour | -23.61382864296989 | -6.358122657801527 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].inc_es | 3.6915034181307815 | 1.6522555869439848 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].inc_std | 0.9700323922865687 | 0.46707800871713473 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].inc_worst | -5.848911864880284 | -2.7456916894400596 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].max_abs_inventory | 4.5700000000001255 | 4.273999999999991 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].max_drawdown | 286.1266630151869 | 85.0561956790158 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].net_bp_per_notional | -1.0114731893536086 | -1.0144913621925014 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].net_per_hour | -13.01918676001399 | -3.5392754550068943 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].net_per_hour_over_inc_std | -11.67025431795389 | -6.989192327119419 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].orders_per_fill | 0.5210985444820748 | 0.9336565996353686 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].own_edge_bp | 0.34828549422731414 | 0.5202057219072382 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].own_markout_1s_bp | -1.5458327662960236 | -1.5684675609161935 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].own_markout_30s_bp | -1.8048812964870247 | -1.814447186227311 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].own_markout_5s_bp | -1.7265616264886972 | -1.7507816787259578 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].paced_spells | 5783.4 | 1081.4 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].paced_time_share | 0.019130553028848935 | 0.0031644439796456704 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].quote_presence_ask | 0.7887066644624632 | 0.8090150197302801 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].quote_presence_bid | 0.7697033419084127 | 0.8275795134589675 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].quote_presence_both | 0.5765648485808474 | 0.6420904949405 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].turnover_per_hour | 132595.24761568726 | 35335.748784804164 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].tw_abs_inventory_avg | 2.271311519502789 | 2.1774661141467315 |
| descriptive.scenarios[P1/conservative/tokyo/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/conservative/tokyo/vip0].fill_rate | 0.2724341681342205 | 0.20721984592367065 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P1/conservative/tokyo/vip0].gross_bp_per_notional | -1.810518700750368 | -1.8106715989945201 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].gross_per_hour | -23.61382864296989 | -6.358122657801527 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].inc_es | 28.17051296600089 | 10.562457691066621 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].inc_std | 6.031945240495702 | 2.447452784902217 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].inc_worst | -35.36368714000584 | -15.716863806000138 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].max_abs_inventory | 4.5700000000001255 | 4.273999999999991 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].max_drawdown | 3400.039408436912 | 999.7112880580122 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].net_bp_per_notional | -11.81466865119924 | -11.8272792650727 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].net_per_hour | -156.26550202517492 | -41.72870926864787 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].net_per_hour_over_inc_std | -22.990026428466905 | -15.717948172542558 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].orders_per_fill | 0.5210985444820748 | 0.9336565996353686 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].own_edge_bp | 0.34828549422731414 | 0.5202057219072382 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].own_markout_1s_bp | -1.5458327662960236 | -1.5684675609161935 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].own_markout_30s_bp | -1.8048812964870247 | -1.814447186227311 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].own_markout_5s_bp | -1.7265616264886972 | -1.7507816787259578 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].paced_spells | 5783.4 | 1081.4 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].paced_time_share | 0.019130553028848935 | 0.0031644439796456704 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].quote_presence_ask | 0.7887066644624632 | 0.8090150197302801 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].quote_presence_bid | 0.7697033419084127 | 0.8275795134589675 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].quote_presence_both | 0.5765648485808474 | 0.6420904949405 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].turnover_per_hour | 132595.24761568726 | 35335.748784804164 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].tw_abs_inventory_avg | 2.271311519502789 | 2.1774661141467315 |
| descriptive.scenarios[P1/conservative/tokyo/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/conservative/tokyo/vip9].fill_rate | 0.2724341681342205 | 0.20721984592367065 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P1/conservative/tokyo/vip9].gross_bp_per_notional | -1.810518700750368 | -1.8106715989945201 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].gross_per_hour | -23.61382864296989 | -6.358122657801527 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].inc_es | 7.600026360061129 | 3.02310568844666 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].inc_std | 1.6824208527220779 | 0.7328586430599561 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].inc_worst | -10.74456144791111 | -4.57651510014005 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].max_abs_inventory | 4.5700000000001255 | 4.273999999999991 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].max_drawdown | 833.6925501055578 | 245.61605877453871 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].net_bp_per_notional | -2.9114731893536083 | -2.9144913621925013 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].net_per_hour | -38.21228380699457 | -10.253067724119685 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].net_per_hour_over_inc_std | -19.79488117604449 | -12.86244001142633 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].orders_per_fill | 0.5210985444820748 | 0.9336565996353686 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].own_edge_bp | 0.34828549422731414 | 0.5202057219072382 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].own_markout_1s_bp | -1.5458327662960236 | -1.5684675609161935 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].own_markout_30s_bp | -1.8048812964870247 | -1.814447186227311 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].own_markout_5s_bp | -1.7265616264886972 | -1.7507816787259578 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].paced_spells | 5783.4 | 1081.4 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].paced_time_share | 0.019130553028848935 | 0.0031644439796456704 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].quote_presence_ask | 0.7887066644624632 | 0.8090150197302801 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].quote_presence_bid | 0.7697033419084127 | 0.8275795134589675 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].quote_presence_both | 0.5765648485808474 | 0.6420904949405 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].turnover_per_hour | 132595.24761568726 | 35335.748784804164 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].tw_abs_inventory_avg | 2.271311519502789 | 2.1774661141467315 |
| descriptive.scenarios[P1/conservative/tokyo/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].fill_rate | 0.3214317244936632 | 0.29719255930416233 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].gross_bp_per_notional | -1.4504807875659629 | -1.4091939726574247 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].gross_per_hour | -17.893514640757385 | -6.077940147352008 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].inc_es | 2.966104061366244 | 1.436148734538571 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].inc_std | 0.8311464378290093 | 0.42017206150497943 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].inc_worst | -5.384695337360093 | -2.5618496703999654 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].max_abs_inventory | 4.748100000000144 | 4.804199999999993 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].max_drawdown | 184.51242242260074 | 63.846341044796716 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].net_bp_per_notional | -0.6514033120302815 | -0.6111785821620505 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].net_per_hour | -8.348169415595198 | -2.644697675302919 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].net_per_hour_over_inc_std | -8.491690850178838 | -5.8161369173816215 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].orders_per_fill | 0.6284931534869344 | 0.9198060403370889 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].own_edge_bp | 0.2723611268760378 | 0.34963741909756096 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].own_markout_1s_bp | -1.1224715942628163 | -1.1324784957627052 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].own_markout_30s_bp | -1.4315898615865528 | -1.3975078046371237 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].own_markout_5s_bp | -1.3208220517704157 | -1.3410007899038963 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].paced_spells | 5806.6 | 1148.8 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].paced_time_share | 0.018972901612620333 | 0.003373996349674572 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].quote_presence_ask | 0.785822978521011 | 0.8207276370804472 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].quote_presence_bid | 0.8027767334152847 | 0.8242492089498323 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].quote_presence_both | 0.615877822343049 | 0.6551502530076289 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].turnover_per_hour | 119467.58898603418 | 42999.49640609663 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].tw_abs_inventory_avg | 2.0958319283547624 | 2.1057832354588792 |
| descriptive.scenarios[P1/intermediate/distant/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/intermediate/distant/vip0].fill_rate | 0.3214317244936632 | 0.29719255930416233 |
| descriptive.scenarios[P1/intermediate/distant/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P1/intermediate/distant/vip0].gross_bp_per_notional | -1.4504807875659629 | -1.4091939726574247 |
| descriptive.scenarios[P1/intermediate/distant/vip0].gross_per_hour | -17.893514640757385 | -6.077940147352008 |
| descriptive.scenarios[P1/intermediate/distant/vip0].inc_es | 21.83905680624556 | 11.302553224800162 |
| descriptive.scenarios[P1/intermediate/distant/vip0].inc_std | 4.461142394353018 | 2.4675342697810576 |
| descriptive.scenarios[P1/intermediate/distant/vip0].inc_worst | -26.117026643998223 | -15.37616615400007 |
| descriptive.scenarios[P1/intermediate/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/intermediate/distant/vip0].max_abs_inventory | 4.748100000000144 | 4.804199999999993 |
| descriptive.scenarios[P1/intermediate/distant/vip0].max_drawdown | 3008.842050757833 | 1176.0827609700168 |
| descriptive.scenarios[P1/intermediate/distant/vip0].net_bp_per_notional | -11.454491763497781 | -11.417822709634057 |
| descriptive.scenarios[P1/intermediate/distant/vip0].net_per_hour | -137.41354664296787 | -49.10664194666012 |
| descriptive.scenarios[P1/intermediate/distant/vip0].net_per_hour_over_inc_std | -27.828377080358514 | -18.62036401748052 |
| descriptive.scenarios[P1/intermediate/distant/vip0].orders_per_fill | 0.6284931534869344 | 0.9198060403370889 |
| descriptive.scenarios[P1/intermediate/distant/vip0].own_edge_bp | 0.2723611268760378 | 0.34963741909756096 |
| descriptive.scenarios[P1/intermediate/distant/vip0].own_markout_1s_bp | -1.1224715942628163 | -1.1324784957627052 |
| descriptive.scenarios[P1/intermediate/distant/vip0].own_markout_30s_bp | -1.4315898615865528 | -1.3975078046371237 |
| descriptive.scenarios[P1/intermediate/distant/vip0].own_markout_5s_bp | -1.3208220517704157 | -1.3410007899038963 |
| descriptive.scenarios[P1/intermediate/distant/vip0].paced_spells | 5806.6 | 1148.8 |
| descriptive.scenarios[P1/intermediate/distant/vip0].paced_time_share | 0.018972901612620333 | 0.003373996349674572 |
| descriptive.scenarios[P1/intermediate/distant/vip0].quote_presence_ask | 0.785822978521011 | 0.8207276370804472 |
| descriptive.scenarios[P1/intermediate/distant/vip0].quote_presence_bid | 0.8027767334152847 | 0.8242492089498323 |
| descriptive.scenarios[P1/intermediate/distant/vip0].quote_presence_both | 0.615877822343049 | 0.6551502530076289 |
| descriptive.scenarios[P1/intermediate/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P1/intermediate/distant/vip0].turnover_per_hour | 119467.58898603418 | 42999.49640609663 |
| descriptive.scenarios[P1/intermediate/distant/vip0].tw_abs_inventory_avg | 2.0958319283547624 | 2.1057832354588792 |
| descriptive.scenarios[P1/intermediate/distant/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/intermediate/distant/vip9].fill_rate | 0.3214317244936632 | 0.29719255930416233 |
| descriptive.scenarios[P1/intermediate/distant/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P1/intermediate/distant/vip9].gross_bp_per_notional | -1.4504807875659629 | -1.4091939726574247 |
| descriptive.scenarios[P1/intermediate/distant/vip9].gross_per_hour | -17.893514640757385 | -6.077940147352008 |
| descriptive.scenarios[P1/intermediate/distant/vip9].inc_es | 5.92148042624916 | 2.9447514878106196 |
| descriptive.scenarios[P1/intermediate/distant/vip9].inc_std | 1.2722204767468688 | 0.6906702550032406 |
| descriptive.scenarios[P1/intermediate/distant/vip9].inc_worst | -8.551473366578042 | -4.422917192959663 |
| descriptive.scenarios[P1/intermediate/distant/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/intermediate/distant/vip9].max_abs_inventory | 4.748100000000144 | 4.804199999999993 |
| descriptive.scenarios[P1/intermediate/distant/vip9].max_drawdown | 681.018728267141 | 258.98198574446013 |
| descriptive.scenarios[P1/intermediate/distant/vip9].net_bp_per_notional | -2.5514033120302817 | -2.5111785821620507 |
| descriptive.scenarios[P1/intermediate/distant/vip9].net_per_hour | -31.047011322941692 | -10.814601992461279 |
| descriptive.scenarios[P1/intermediate/distant/vip9].net_per_hour_over_inc_std | -21.535619357745272 | -14.519447947356564 |
| descriptive.scenarios[P1/intermediate/distant/vip9].orders_per_fill | 0.6284931534869344 | 0.9198060403370889 |
| descriptive.scenarios[P1/intermediate/distant/vip9].own_edge_bp | 0.2723611268760378 | 0.34963741909756096 |
| descriptive.scenarios[P1/intermediate/distant/vip9].own_markout_1s_bp | -1.1224715942628163 | -1.1324784957627052 |
| descriptive.scenarios[P1/intermediate/distant/vip9].own_markout_30s_bp | -1.4315898615865528 | -1.3975078046371237 |
| descriptive.scenarios[P1/intermediate/distant/vip9].own_markout_5s_bp | -1.3208220517704157 | -1.3410007899038963 |
| descriptive.scenarios[P1/intermediate/distant/vip9].paced_spells | 5806.6 | 1148.8 |
| descriptive.scenarios[P1/intermediate/distant/vip9].paced_time_share | 0.018972901612620333 | 0.003373996349674572 |
| descriptive.scenarios[P1/intermediate/distant/vip9].quote_presence_ask | 0.785822978521011 | 0.8207276370804472 |
| descriptive.scenarios[P1/intermediate/distant/vip9].quote_presence_bid | 0.8027767334152847 | 0.8242492089498323 |
| descriptive.scenarios[P1/intermediate/distant/vip9].quote_presence_both | 0.615877822343049 | 0.6551502530076289 |
| descriptive.scenarios[P1/intermediate/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P1/intermediate/distant/vip9].turnover_per_hour | 119467.58898603418 | 42999.49640609663 |
| descriptive.scenarios[P1/intermediate/distant/vip9].tw_abs_inventory_avg | 2.0958319283547624 | 2.1057832354588792 |
| descriptive.scenarios[P1/intermediate/distant/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].fill_rate | 0.3241925548905807 | 0.2880615458764798 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].gross_bp_per_notional | -1.479066923688033 | -1.4197703532040251 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].gross_per_hour | -22.46359752525914 | -6.845774007495038 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].inc_es | 3.242466800542625 | 1.5640429037972807 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].inc_std | 0.8830041797831578 | 0.4561861047925526 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].inc_worst | -5.107629293361114 | -2.9922736952001943 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].max_abs_inventory | 4.852500000000334 | 4.855799999999997 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].max_drawdown | 233.2098603159563 | 72.26808783139668 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].net_bp_per_notional | -0.67994108037458 | -0.6218049257161775 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].net_per_hour | -10.598324002561796 | -2.999912855517848 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].net_per_hour_over_inc_std | -10.190674144587964 | -6.078540438853158 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].orders_per_fill | 0.542765782971256 | 0.8567515656043613 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].own_edge_bp | 0.2352495321717496 | 0.34690355454552224 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].own_markout_1s_bp | -1.178003992517609 | -1.163256233111128 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].own_markout_30s_bp | -1.4573850762854488 | -1.4139522684030004 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].own_markout_5s_bp | -1.3660398233682485 | -1.3660759364318955 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].paced_spells | 6157.8 | 1203.0 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].paced_time_share | 0.020144425008850414 | 0.0035097782998275125 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].quote_presence_ask | 0.7942346645816545 | 0.821647657245727 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].quote_presence_bid | 0.80548321583805 | 0.8311702621867372 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].quote_presence_both | 0.6203096447382651 | 0.6596166441847915 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].turnover_per_hour | 148485.56182047064 | 48159.0350846619 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].tw_abs_inventory_avg | 2.1523939689240614 | 2.128900008101211 |
| descriptive.scenarios[P1/intermediate/regional/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/intermediate/regional/vip0].fill_rate | 0.3241925548905807 | 0.2880615458764798 |
| descriptive.scenarios[P1/intermediate/regional/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P1/intermediate/regional/vip0].gross_bp_per_notional | -1.479066923688033 | -1.4197703532040251 |
| descriptive.scenarios[P1/intermediate/regional/vip0].gross_per_hour | -22.46359752525914 | -6.845774007495038 |
| descriptive.scenarios[P1/intermediate/regional/vip0].inc_es | 28.859633791312934 | 13.094016526933876 |
| descriptive.scenarios[P1/intermediate/regional/vip0].inc_std | 5.973407082970623 | 2.8973202786901444 |
| descriptive.scenarios[P1/intermediate/regional/vip0].inc_worst | -35.258427047993244 | -18.93441719000125 |
| descriptive.scenarios[P1/intermediate/regional/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/intermediate/regional/vip0].max_abs_inventory | 4.852500000000334 | 4.855799999999997 |
| descriptive.scenarios[P1/intermediate/regional/vip0].max_drawdown | 3731.5085348028942 | 1318.100818226028 |
| descriptive.scenarios[P1/intermediate/regional/vip0].net_bp_per_notional | -11.48286760493389 | -11.428616320648166 |
| descriptive.scenarios[P1/intermediate/regional/vip0].net_per_hour | -171.00816553242677 | -55.034642373877645 |
| descriptive.scenarios[P1/intermediate/regional/vip0].net_per_hour_over_inc_std | -25.808021990791183 | -17.711761771838077 |
| descriptive.scenarios[P1/intermediate/regional/vip0].orders_per_fill | 0.542765782971256 | 0.8567515656043613 |
| descriptive.scenarios[P1/intermediate/regional/vip0].own_edge_bp | 0.2352495321717496 | 0.34690355454552224 |
| descriptive.scenarios[P1/intermediate/regional/vip0].own_markout_1s_bp | -1.178003992517609 | -1.163256233111128 |
| descriptive.scenarios[P1/intermediate/regional/vip0].own_markout_30s_bp | -1.4573850762854488 | -1.4139522684030004 |
| descriptive.scenarios[P1/intermediate/regional/vip0].own_markout_5s_bp | -1.3660398233682485 | -1.3660759364318955 |
| descriptive.scenarios[P1/intermediate/regional/vip0].paced_spells | 6157.8 | 1203.0 |
| descriptive.scenarios[P1/intermediate/regional/vip0].paced_time_share | 0.020144425008850414 | 0.0035097782998275125 |
| descriptive.scenarios[P1/intermediate/regional/vip0].quote_presence_ask | 0.7942346645816545 | 0.821647657245727 |
| descriptive.scenarios[P1/intermediate/regional/vip0].quote_presence_bid | 0.80548321583805 | 0.8311702621867372 |
| descriptive.scenarios[P1/intermediate/regional/vip0].quote_presence_both | 0.6203096447382651 | 0.6596166441847915 |
| descriptive.scenarios[P1/intermediate/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P1/intermediate/regional/vip0].turnover_per_hour | 148485.56182047064 | 48159.0350846619 |
| descriptive.scenarios[P1/intermediate/regional/vip0].tw_abs_inventory_avg | 2.1523939689240614 | 2.128900008101211 |
| descriptive.scenarios[P1/intermediate/regional/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/intermediate/regional/vip9].fill_rate | 0.3241925548905807 | 0.2880615458764798 |
| descriptive.scenarios[P1/intermediate/regional/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P1/intermediate/regional/vip9].gross_bp_per_notional | -1.479066923688033 | -1.4197703532040251 |
| descriptive.scenarios[P1/intermediate/regional/vip9].gross_per_hour | -22.46359752525914 | -6.845774007495038 |
| descriptive.scenarios[P1/intermediate/regional/vip9].inc_es | 7.321441050203754 | 3.382523768645386 |
| descriptive.scenarios[P1/intermediate/regional/vip9].inc_std | 1.5833265300795296 | 0.7896920102628854 |
| descriptive.scenarios[P1/intermediate/regional/vip9].inc_worst | -9.859120599828383 | -5.149465672439905 |
| descriptive.scenarios[P1/intermediate/regional/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/intermediate/regional/vip9].max_abs_inventory | 4.852500000000334 | 4.855799999999997 |
| descriptive.scenarios[P1/intermediate/regional/vip9].max_drawdown | 848.3310035793717 | 290.9808955831021 |
| descriptive.scenarios[P1/intermediate/regional/vip9].net_bp_per_notional | -2.57994108037458 | -2.521804925716178 |
| descriptive.scenarios[P1/intermediate/regional/vip9].net_per_hour | -38.810580748451216 | -12.150129521603608 |
| descriptive.scenarios[P1/intermediate/regional/vip9].net_per_hour_over_inc_std | -21.615941249498885 | -14.250882530927152 |
| descriptive.scenarios[P1/intermediate/regional/vip9].orders_per_fill | 0.542765782971256 | 0.8567515656043613 |
| descriptive.scenarios[P1/intermediate/regional/vip9].own_edge_bp | 0.2352495321717496 | 0.34690355454552224 |
| descriptive.scenarios[P1/intermediate/regional/vip9].own_markout_1s_bp | -1.178003992517609 | -1.163256233111128 |
| descriptive.scenarios[P1/intermediate/regional/vip9].own_markout_30s_bp | -1.4573850762854488 | -1.4139522684030004 |
| descriptive.scenarios[P1/intermediate/regional/vip9].own_markout_5s_bp | -1.3660398233682485 | -1.3660759364318955 |
| descriptive.scenarios[P1/intermediate/regional/vip9].paced_spells | 6157.8 | 1203.0 |
| descriptive.scenarios[P1/intermediate/regional/vip9].paced_time_share | 0.020144425008850414 | 0.0035097782998275125 |
| descriptive.scenarios[P1/intermediate/regional/vip9].quote_presence_ask | 0.7942346645816545 | 0.821647657245727 |
| descriptive.scenarios[P1/intermediate/regional/vip9].quote_presence_bid | 0.80548321583805 | 0.8311702621867372 |
| descriptive.scenarios[P1/intermediate/regional/vip9].quote_presence_both | 0.6203096447382651 | 0.6596166441847915 |
| descriptive.scenarios[P1/intermediate/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P1/intermediate/regional/vip9].turnover_per_hour | 148485.56182047064 | 48159.0350846619 |
| descriptive.scenarios[P1/intermediate/regional/vip9].tw_abs_inventory_avg | 2.1523939689240614 | 2.128900008101211 |
| descriptive.scenarios[P1/intermediate/regional/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].fill_rate | 0.3236398239260895 | 0.269258543781509 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].gross_bp_per_notional | -1.6148796800329865 | -1.5307672728590305 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].gross_per_hour | -26.21761966625205 | -7.523365109195533 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].inc_es | 3.681452723986003 | 1.5791592012906688 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].inc_std | 0.9628988677899308 | 0.4593602983977204 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].inc_worst | -5.623103282160503 | -2.5671095049596104 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].max_abs_inventory | 4.444600000000138 | 4.32900000000001 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].max_drawdown | 292.6465970358854 | 86.95914231395426 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].net_bp_per_notional | -0.8155970808675257 | -0.7326758642100664 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].net_per_hour | -13.325550424511468 | -3.6138477674259177 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].net_per_hour_over_inc_std | -11.97750953834225 | -7.25613179649312 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].orders_per_fill | 0.518405820560484 | 0.8722049236216189 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].own_edge_bp | 0.3632250200445307 | 0.5369183695586928 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].own_markout_1s_bp | -1.3223481027147193 | -1.2865329330503326 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].own_markout_30s_bp | -1.5944369371245195 | -1.5304420367679756 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].own_markout_5s_bp | -1.5115554802888902 | -1.4812620577898703 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].paced_spells | 6204.1 | 1259.0 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].paced_time_share | 0.02045469409779442 | 0.0037315848589133315 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].quote_presence_ask | 0.7855455134143975 | 0.821341547135815 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].quote_presence_bid | 0.7802061138727421 | 0.8173754987076777 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].quote_presence_both | 0.5847517627622546 | 0.6446061830123508 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].turnover_per_hour | 161303.71505484433 | 48952.15361752708 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].tw_abs_inventory_avg | 2.2509379995765015 | 2.179840147770156 |
| descriptive.scenarios[P1/intermediate/tokyo/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].fill_rate | 0.3236398239260895 | 0.269258543781509 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].gross_bp_per_notional | -1.6148796800329865 | -1.5307672728590305 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].gross_per_hour | -26.21761966625205 | -7.523365109195533 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].inc_es | 30.796191798419404 | 12.890658656400259 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].inc_std | 6.380391145243139 | 2.8711791417945394 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].inc_worst | -37.66491196600252 | -18.046962548001822 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].max_abs_inventory | 4.444600000000138 | 4.32900000000001 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].max_drawdown | 4087.7002569759593 | 1353.4566607320307 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].net_bp_per_notional | -11.6179988140962 | -11.539065496124405 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].net_per_hour | -187.57449977608314 | -56.50445328164674 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].net_per_hour_over_inc_std | -26.509291158440078 | -18.307919230211958 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].orders_per_fill | 0.518405820560484 | 0.8722049236216189 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].own_edge_bp | 0.3632250200445307 | 0.5369183695586928 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].own_markout_1s_bp | -1.3223481027147193 | -1.2865329330503326 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].own_markout_30s_bp | -1.5944369371245195 | -1.5304420367679756 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].own_markout_5s_bp | -1.5115554802888902 | -1.4812620577898703 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].paced_spells | 6204.1 | 1259.0 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].paced_time_share | 0.02045469409779442 | 0.0037315848589133315 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].quote_presence_ask | 0.7855455134143975 | 0.821341547135815 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].quote_presence_bid | 0.7802061138727421 | 0.8173754987076777 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].quote_presence_both | 0.5847517627622546 | 0.6446061830123508 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].turnover_per_hour | 161303.71505484433 | 48952.15361752708 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].tw_abs_inventory_avg | 2.2509379995765015 | 2.179840147770156 |
| descriptive.scenarios[P1/intermediate/tokyo/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].fill_rate | 0.3236398239260895 | 0.269258543781509 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].gross_bp_per_notional | -1.6148796800329865 | -1.5307672728590305 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].gross_per_hour | -26.21761966625205 | -7.523365109195533 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].inc_es | 8.03222982974721 | 3.3438313820719614 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].inc_std | 1.7237088269874554 | 0.7854166259916592 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].inc_worst | -10.798876565920338 | -4.92237725720012 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].max_abs_inventory | 4.444600000000138 | 4.32900000000001 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].max_drawdown | 960.0551719215825 | 309.33540228356077 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].net_bp_per_notional | -2.715597080867526 | -2.6326758642100665 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].net_per_hour | -43.973256284931885 | -12.914756954756063 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].net_per_hour_over_inc_std | -22.566839272247865 | -15.228404518647011 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].orders_per_fill | 0.518405820560484 | 0.8722049236216189 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].own_edge_bp | 0.3632250200445307 | 0.5369183695586928 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].own_markout_1s_bp | -1.3223481027147193 | -1.2865329330503326 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].own_markout_30s_bp | -1.5944369371245195 | -1.5304420367679756 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].own_markout_5s_bp | -1.5115554802888902 | -1.4812620577898703 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].paced_spells | 6204.1 | 1259.0 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].paced_time_share | 0.02045469409779442 | 0.0037315848589133315 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].quote_presence_ask | 0.7855455134143975 | 0.821341547135815 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].quote_presence_bid | 0.7802061138727421 | 0.8173754987076777 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].quote_presence_both | 0.5847517627622546 | 0.6446061830123508 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].turnover_per_hour | 161303.71505484433 | 48952.15361752708 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].tw_abs_inventory_avg | 2.2509379995765015 | 2.179840147770156 |
| descriptive.scenarios[P1/intermediate/tokyo/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].fill_rate | 0.4450978966284989 | 0.4657755509684093 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].gross_bp_per_notional | -1.0934790421045373 | -0.9865410835627229 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].gross_per_hour | -19.214917115269728 | -7.3835310985846245 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].inc_es | 2.6847621493066334 | 1.2239809346451682 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].inc_std | 0.8168153231497761 | 0.4006884877644306 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].inc_worst | -4.6951295704004865 | -2.0250791943997073 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].max_abs_inventory | 4.571800000000058 | 3.9966000000000053 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].max_drawdown | 132.78200728509725 | 40.844478732815375 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].net_bp_per_notional | -0.2940186765971649 | -0.1877139829832787 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].net_per_hour | -5.923935717783631 | -1.585234219821871 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].net_per_hour_over_inc_std | -5.756242995726721 | -3.498417985359832 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].orders_per_fill | 0.5640646690736586 | 0.7507290961032972 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].own_edge_bp | 0.4180279048915755 | 0.5806296776871881 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].own_markout_1s_bp | -0.7848241629453261 | -0.733229544979473 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].own_markout_30s_bp | -1.073593542241864 | -0.9702638793815183 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].own_markout_5s_bp | -0.9700745453701709 | -0.9309481133211872 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].paced_spells | 7289.3 | 1723.2 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].paced_time_share | 0.023767782573246445 | 0.005113988448860518 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].quote_presence_ask | 0.7530184274193616 | 0.8061150316479682 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].quote_presence_bid | 0.7912097776586473 | 0.8045045372786005 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].quote_presence_both | 0.579323990129599 | 0.6251818250833123 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].turnover_per_hour | 166273.69610797346 | 72561.91077620783 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].tw_abs_inventory_avg | 2.112009112045624 | 2.0833008313541077 |
| descriptive.scenarios[P1/optimistic/distant/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/optimistic/distant/vip0].fill_rate | 0.4450978966284989 | 0.4657755509684093 |
| descriptive.scenarios[P1/optimistic/distant/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P1/optimistic/distant/vip0].gross_bp_per_notional | -1.0934790421045373 | -0.9865410835627229 |
| descriptive.scenarios[P1/optimistic/distant/vip0].gross_per_hour | -19.214917115269728 | -7.3835310985846245 |
| descriptive.scenarios[P1/optimistic/distant/vip0].inc_es | 26.919841497364395 | 16.39180180360001 |
| descriptive.scenarios[P1/optimistic/distant/vip0].inc_std | 5.278775968019572 | 3.4960367469754763 |
| descriptive.scenarios[P1/optimistic/distant/vip0].inc_worst | -30.882991272002243 | -19.813173014000434 |
| descriptive.scenarios[P1/optimistic/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/optimistic/distant/vip0].max_abs_inventory | 4.571800000000058 | 3.9966000000000053 |
| descriptive.scenarios[P1/optimistic/distant/vip0].max_drawdown | 4078.6891120340165 | 1914.9722890619846 |
| descriptive.scenarios[P1/optimistic/distant/vip0].net_bp_per_notional | -11.095825279029006 | -10.991640646260793 |
| descriptive.scenarios[P1/optimistic/distant/vip0].net_per_hour | -185.53606666303355 | -79.97438093276583 |
| descriptive.scenarios[P1/optimistic/distant/vip0].net_per_hour_over_inc_std | -32.24316596634695 | -21.598577729074975 |
| descriptive.scenarios[P1/optimistic/distant/vip0].orders_per_fill | 0.5640646690736586 | 0.7507290961032972 |
| descriptive.scenarios[P1/optimistic/distant/vip0].own_edge_bp | 0.4180279048915755 | 0.5806296776871881 |
| descriptive.scenarios[P1/optimistic/distant/vip0].own_markout_1s_bp | -0.7848241629453261 | -0.733229544979473 |
| descriptive.scenarios[P1/optimistic/distant/vip0].own_markout_30s_bp | -1.073593542241864 | -0.9702638793815183 |
| descriptive.scenarios[P1/optimistic/distant/vip0].own_markout_5s_bp | -0.9700745453701709 | -0.9309481133211872 |
| descriptive.scenarios[P1/optimistic/distant/vip0].paced_spells | 7289.3 | 1723.2 |
| descriptive.scenarios[P1/optimistic/distant/vip0].paced_time_share | 0.023767782573246445 | 0.005113988448860518 |
| descriptive.scenarios[P1/optimistic/distant/vip0].quote_presence_ask | 0.7530184274193616 | 0.8061150316479682 |
| descriptive.scenarios[P1/optimistic/distant/vip0].quote_presence_bid | 0.7912097776586473 | 0.8045045372786005 |
| descriptive.scenarios[P1/optimistic/distant/vip0].quote_presence_both | 0.579323990129599 | 0.6251818250833123 |
| descriptive.scenarios[P1/optimistic/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P1/optimistic/distant/vip0].turnover_per_hour | 166273.69610797346 | 72561.91077620783 |
| descriptive.scenarios[P1/optimistic/distant/vip0].tw_abs_inventory_avg | 2.112009112045624 | 2.0833008313541077 |
| descriptive.scenarios[P1/optimistic/distant/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/optimistic/distant/vip9].fill_rate | 0.4450978966284989 | 0.4657755509684093 |
| descriptive.scenarios[P1/optimistic/distant/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P1/optimistic/distant/vip9].gross_bp_per_notional | -1.0934790421045373 | -0.9865410835627229 |
| descriptive.scenarios[P1/optimistic/distant/vip9].gross_per_hour | -19.214917115269728 | -7.3835310985846245 |
| descriptive.scenarios[P1/optimistic/distant/vip9].inc_es | 6.505867452961122 | 3.580223276115901 |
| descriptive.scenarios[P1/optimistic/distant/vip9].inc_std | 1.341851060483503 | 0.8114079563075297 |
| descriptive.scenarios[P1/optimistic/distant/vip9].inc_worst | -8.593838834610477 | -4.766491954039958 |
| descriptive.scenarios[P1/optimistic/distant/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/optimistic/distant/vip9].max_abs_inventory | 4.571800000000058 | 3.9966000000000053 |
| descriptive.scenarios[P1/optimistic/distant/vip9].max_drawdown | 825.2498216792432 | 368.0652199259552 |
| descriptive.scenarios[P1/optimistic/distant/vip9].net_bp_per_notional | -2.1940186765971648 | -2.0877139829832787 |
| descriptive.scenarios[P1/optimistic/distant/vip9].net_per_hour | -37.515937978298595 | -15.371997267301358 |
| descriptive.scenarios[P1/optimistic/distant/vip9].net_per_hour_over_inc_std | -25.10782625854103 | -17.641537794930343 |
| descriptive.scenarios[P1/optimistic/distant/vip9].orders_per_fill | 0.5640646690736586 | 0.7507290961032972 |
| descriptive.scenarios[P1/optimistic/distant/vip9].own_edge_bp | 0.4180279048915755 | 0.5806296776871881 |
| descriptive.scenarios[P1/optimistic/distant/vip9].own_markout_1s_bp | -0.7848241629453261 | -0.733229544979473 |
| descriptive.scenarios[P1/optimistic/distant/vip9].own_markout_30s_bp | -1.073593542241864 | -0.9702638793815183 |
| descriptive.scenarios[P1/optimistic/distant/vip9].own_markout_5s_bp | -0.9700745453701709 | -0.9309481133211872 |
| descriptive.scenarios[P1/optimistic/distant/vip9].paced_spells | 7289.3 | 1723.2 |
| descriptive.scenarios[P1/optimistic/distant/vip9].paced_time_share | 0.023767782573246445 | 0.005113988448860518 |
| descriptive.scenarios[P1/optimistic/distant/vip9].quote_presence_ask | 0.7530184274193616 | 0.8061150316479682 |
| descriptive.scenarios[P1/optimistic/distant/vip9].quote_presence_bid | 0.7912097776586473 | 0.8045045372786005 |
| descriptive.scenarios[P1/optimistic/distant/vip9].quote_presence_both | 0.579323990129599 | 0.6251818250833123 |
| descriptive.scenarios[P1/optimistic/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P1/optimistic/distant/vip9].turnover_per_hour | 166273.69610797346 | 72561.91077620783 |
| descriptive.scenarios[P1/optimistic/distant/vip9].tw_abs_inventory_avg | 2.112009112045624 | 2.0833008313541077 |
| descriptive.scenarios[P1/optimistic/distant/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].fill_rate | 0.5234837058030946 | 0.5311652078963636 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].gross_bp_per_notional | -1.1536315535032153 | -1.0710556658407362 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].gross_per_hour | -28.76256573879446 | -10.49225995338374 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].inc_es | 3.273150752813875 | 1.5812776359999767 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].inc_std | 0.9193735565524964 | 0.47879973750506055 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].inc_worst | -5.397388549280308 | -2.9060790863999224 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].max_abs_inventory | 4.498900000000102 | 4.1888000000000085 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].max_drawdown | 215.53425657006505 | 70.78129518632417 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].net_bp_per_notional | -0.35408087920956804 | -0.2716272218232981 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].net_per_hour | -9.755479756442858 | -2.8606433460713823 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].net_per_hour_over_inc_std | -8.629484346429873 | -5.356742331375036 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].orders_per_fill | 0.496743260332232 | 0.6761033107399579 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].own_edge_bp | 0.41229619274596024 | 0.5776526696006625 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].own_markout_1s_bp | -0.8688014141994964 | -0.8177082606352994 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].own_markout_30s_bp | -1.1356799029996052 | -1.0692352052503569 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].own_markout_5s_bp | -1.0499362021464083 | -1.0189555458882658 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].paced_spells | 8722.3 | 2032.6 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].paced_time_share | 0.02853021952512676 | 0.006012375112828015 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].quote_presence_ask | 0.7485835601988586 | 0.7996993862686729 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].quote_presence_bid | 0.7798721950844683 | 0.8004194629036985 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].quote_presence_both | 0.5571011208171753 | 0.6098378179400439 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].turnover_per_hour | 237743.14730193117 | 95453.1391173123 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].tw_abs_inventory_avg | 2.234680668429341 | 2.1790128237326565 |
| descriptive.scenarios[P1/optimistic/regional/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/optimistic/regional/vip0].fill_rate | 0.5234837058030946 | 0.5311652078963636 |
| descriptive.scenarios[P1/optimistic/regional/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P1/optimistic/regional/vip0].gross_bp_per_notional | -1.1536315535032153 | -1.0710556658407362 |
| descriptive.scenarios[P1/optimistic/regional/vip0].gross_per_hour | -28.76256573879446 | -10.49225995338374 |
| descriptive.scenarios[P1/optimistic/regional/vip0].inc_es | 40.1118488114323 | 22.84373289199914 |
| descriptive.scenarios[P1/optimistic/regional/vip0].inc_std | 8.051817673987312 | 4.9509419905330105 |
| descriptive.scenarios[P1/optimistic/regional/vip0].inc_worst | -46.71162202399126 | -28.607531358000596 |
| descriptive.scenarios[P1/optimistic/regional/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/optimistic/regional/vip0].max_abs_inventory | 4.498900000000102 | 4.1888000000000085 |
| descriptive.scenarios[P1/optimistic/regional/vip0].max_drawdown | 5841.790647512028 | 2537.3158156498985 |
| descriptive.scenarios[P1/optimistic/regional/vip0].net_bp_per_notional | -11.155585143530836 | -11.073540691851875 |
| descriptive.scenarios[P1/optimistic/regional/vip0].net_per_hour | -266.5594773963904 | -105.96554916666398 |
| descriptive.scenarios[P1/optimistic/regional/vip0].net_per_hour_over_inc_std | -30.018227539194594 | -20.113324852074943 |
| descriptive.scenarios[P1/optimistic/regional/vip0].orders_per_fill | 0.496743260332232 | 0.6761033107399579 |
| descriptive.scenarios[P1/optimistic/regional/vip0].own_edge_bp | 0.41229619274596024 | 0.5776526696006625 |
| descriptive.scenarios[P1/optimistic/regional/vip0].own_markout_1s_bp | -0.8688014141994964 | -0.8177082606352994 |
| descriptive.scenarios[P1/optimistic/regional/vip0].own_markout_30s_bp | -1.1356799029996052 | -1.0692352052503569 |
| descriptive.scenarios[P1/optimistic/regional/vip0].own_markout_5s_bp | -1.0499362021464083 | -1.0189555458882658 |
| descriptive.scenarios[P1/optimistic/regional/vip0].paced_spells | 8722.3 | 2032.6 |
| descriptive.scenarios[P1/optimistic/regional/vip0].paced_time_share | 0.02853021952512676 | 0.006012375112828015 |
| descriptive.scenarios[P1/optimistic/regional/vip0].quote_presence_ask | 0.7485835601988586 | 0.7996993862686729 |
| descriptive.scenarios[P1/optimistic/regional/vip0].quote_presence_bid | 0.7798721950844683 | 0.8004194629036985 |
| descriptive.scenarios[P1/optimistic/regional/vip0].quote_presence_both | 0.5571011208171753 | 0.6098378179400439 |
| descriptive.scenarios[P1/optimistic/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P1/optimistic/regional/vip0].turnover_per_hour | 237743.14730193117 | 95453.1391173123 |
| descriptive.scenarios[P1/optimistic/regional/vip0].tw_abs_inventory_avg | 2.234680668429341 | 2.1790128237326565 |
| descriptive.scenarios[P1/optimistic/regional/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/optimistic/regional/vip9].fill_rate | 0.5234837058030946 | 0.5311652078963636 |
| descriptive.scenarios[P1/optimistic/regional/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P1/optimistic/regional/vip9].gross_bp_per_notional | -1.1536315535032153 | -1.0710556658407362 |
| descriptive.scenarios[P1/optimistic/regional/vip9].gross_per_hour | -28.76256573879446 | -10.49225995338374 |
| descriptive.scenarios[P1/optimistic/regional/vip9].inc_es | 9.225617963242307 | 5.078290515558612 |
| descriptive.scenarios[P1/optimistic/regional/vip9].inc_std | 1.9045066752334918 | 1.1437660652884172 |
| descriptive.scenarios[P1/optimistic/regional/vip9].inc_worst | -12.132075188637861 | -6.969506169599541 |
| descriptive.scenarios[P1/optimistic/regional/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/optimistic/regional/vip9].max_abs_inventory | 4.498900000000102 | 4.1888000000000085 |
| descriptive.scenarios[P1/optimistic/regional/vip9].max_drawdown | 1204.241077762728 | 502.752882915447 |
| descriptive.scenarios[P1/optimistic/regional/vip9].net_bp_per_notional | -2.2540808792095683 | -2.1716272218232984 |
| descriptive.scenarios[P1/optimistic/regional/vip9].net_per_hour | -54.92667774380978 | -20.99673977836072 |
| descriptive.scenarios[P1/optimistic/regional/vip9].net_per_hour_over_inc_std | -25.707499306322454 | -17.079738056149985 |
| descriptive.scenarios[P1/optimistic/regional/vip9].orders_per_fill | 0.496743260332232 | 0.6761033107399579 |
| descriptive.scenarios[P1/optimistic/regional/vip9].own_edge_bp | 0.41229619274596024 | 0.5776526696006625 |
| descriptive.scenarios[P1/optimistic/regional/vip9].own_markout_1s_bp | -0.8688014141994964 | -0.8177082606352994 |
| descriptive.scenarios[P1/optimistic/regional/vip9].own_markout_30s_bp | -1.1356799029996052 | -1.0692352052503569 |
| descriptive.scenarios[P1/optimistic/regional/vip9].own_markout_5s_bp | -1.0499362021464083 | -1.0189555458882658 |
| descriptive.scenarios[P1/optimistic/regional/vip9].paced_spells | 8722.3 | 2032.6 |
| descriptive.scenarios[P1/optimistic/regional/vip9].paced_time_share | 0.02853021952512676 | 0.006012375112828015 |
| descriptive.scenarios[P1/optimistic/regional/vip9].quote_presence_ask | 0.7485835601988586 | 0.7996993862686729 |
| descriptive.scenarios[P1/optimistic/regional/vip9].quote_presence_bid | 0.7798721950844683 | 0.8004194629036985 |
| descriptive.scenarios[P1/optimistic/regional/vip9].quote_presence_both | 0.5571011208171753 | 0.6098378179400439 |
| descriptive.scenarios[P1/optimistic/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P1/optimistic/regional/vip9].turnover_per_hour | 237743.14730193117 | 95453.1391173123 |
| descriptive.scenarios[P1/optimistic/regional/vip9].tw_abs_inventory_avg | 2.234680668429341 | 2.1790128237326565 |
| descriptive.scenarios[P1/optimistic/regional/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].fill_rate | 0.5524194819343494 | 0.5615164709030518 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].gate_active_share | None | undefined |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].gross_bp_per_notional | -1.3041613844641928 | -1.2167072025286216 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].gross_per_hour | -37.04691297000551 | -13.797493685868508 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].inc_es | 4.002639055128349 | 1.909727294741487 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].inc_std | 1.0372396959949843 | 0.544743433477009 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].inc_worst | -5.93190063400122 | -3.1072269297603183 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].max_abs_inventory | 4.182399999999928 | 3.9981999999999807 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].max_drawdown | 332.01777222503034 | 118.93742803556657 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].net_bp_per_notional | -0.5045633031310521 | -0.41735085011942613 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].net_per_hour | -15.051278544927573 | -4.914710854031224 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].net_per_hour_over_inc_std | -12.30674140782524 | -8.204947278655965 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].orders_per_fill | 0.41219187389473316 | 0.5626400487849115 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].own_edge_bp | 0.4112533427670451 | 0.5771794094196847 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].own_markout_1s_bp | -1.0238805261470005 | -0.9642833592888376 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].own_markout_30s_bp | -1.2874950401166467 | -1.2089990049378874 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].own_markout_5s_bp | -1.2066156193335251 | -1.1652580522853884 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].paced_spells | 7657.5 | 1671.2 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].paced_time_share | 0.02471614154248474 | 0.004828150613238612 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].quote_presence_ask | 0.741788083274696 | 0.7858743677148876 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].quote_presence_bid | 0.7606579543535954 | 0.7877300519920631 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].quote_presence_both | 0.5248748972507656 | 0.5803946719299186 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].turnover_per_hour | 275103.6573961958 | 111104.66682689951 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].tw_abs_inventory_avg | 2.3515003271504886 | 2.2748594515063547 |
| descriptive.scenarios[P1/optimistic/tokyo/lp_tier4].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].fill_rate | 0.5524194819343494 | 0.5615164709030518 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].gate_active_share | None | undefined |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].gross_bp_per_notional | -1.3041613844641928 | -1.2167072025286216 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].gross_per_hour | -37.04691297000551 | -13.797493685868508 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].inc_es | 45.99340417572056 | 26.919447901599817 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].inc_std | 9.56124179949103 | 5.872160865858354 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].inc_worst | -53.268915184005266 | -32.96902224399496 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].max_abs_inventory | 4.182399999999928 | 3.9981999999999807 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].max_drawdown | 6849.001931432028 | 2991.539241935908 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].net_bp_per_notional | -11.305908856928799 | -11.219505670314728 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].net_per_hour | -312.20560587323496 | -124.92646709674491 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].net_per_hour_over_inc_std | -29.514549675302458 | -19.940182598434973 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].orders_per_fill | 0.41219187389473316 | 0.5626400487849115 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].own_edge_bp | 0.4112533427670451 | 0.5771794094196847 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].own_markout_1s_bp | -1.0238805261470005 | -0.9642833592888376 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].own_markout_30s_bp | -1.2874950401166467 | -1.2089990049378874 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].own_markout_5s_bp | -1.2066156193335251 | -1.1652580522853884 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].paced_spells | 7657.5 | 1671.2 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].paced_time_share | 0.02471614154248474 | 0.004828150613238612 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].quote_presence_ask | 0.741788083274696 | 0.7858743677148876 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].quote_presence_bid | 0.7606579543535954 | 0.7877300519920631 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].quote_presence_both | 0.5248748972507656 | 0.5803946719299186 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].turnover_per_hour | 275103.6573961958 | 111104.66682689951 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].tw_abs_inventory_avg | 2.3515003271504886 | 2.2748594515063547 |
| descriptive.scenarios[P1/optimistic/tokyo/vip0].vol_closed_share | None | undefined |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].fill_rate | 0.5524194819343494 | 0.5615164709030518 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].gate_active_share | None | undefined |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].gross_bp_per_notional | -1.3041613844641928 | -1.2167072025286216 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].gross_per_hour | -37.04691297000551 | -13.797493685868508 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].inc_es | 10.82110631044837 | 6.037917630819964 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].inc_std | 2.2822438535954865 | 1.3701877280751888 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].inc_worst | -13.579704038020973 | -8.046928238779584 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].max_abs_inventory | 4.182399999999928 | 3.9981999999999807 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].max_drawdown | 1478.2353662287408 | 623.1929148367103 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].net_bp_per_notional | -2.4045633031310523 | -2.317350850119426 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].net_per_hour | -67.32097345020478 | -26.02459755114213 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].net_per_hour_over_inc_std | -26.318693564613834 | -17.665768769797214 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].orders_per_fill | 0.41219187389473316 | 0.5626400487849115 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].own_edge_bp | 0.4112533427670451 | 0.5771794094196847 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].own_markout_1s_bp | -1.0238805261470005 | -0.9642833592888376 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].own_markout_30s_bp | -1.2874950401166467 | -1.2089990049378874 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].own_markout_5s_bp | -1.2066156193335251 | -1.1652580522853884 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].paced_spells | 7657.5 | 1671.2 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].paced_time_share | 0.02471614154248474 | 0.004828150613238612 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].quote_presence_ask | 0.741788083274696 | 0.7858743677148876 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].quote_presence_bid | 0.7606579543535954 | 0.7877300519920631 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].quote_presence_both | 0.5248748972507656 | 0.5803946719299186 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].turnover_per_hour | 275103.6573961958 | 111104.66682689951 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].tw_abs_inventory_avg | 2.3515003271504886 | 2.2748594515063547 |
| descriptive.scenarios[P1/optimistic/tokyo/vip9].vol_closed_share | None | undefined |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].fill_rate | 0.2835309765879449 | 0.2527208275640717 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].gate_active_share | 0.013975445835994405 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].gross_bp_per_notional | -1.640226909584738 | -1.6225467157075042 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].gross_per_hour | -18.456288337737075 | -6.120964304303366 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].inc_es | 6.187435045196476 | 3.021887453343707 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].inc_std | 1.9477079302985867 | 0.9782534097709163 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].inc_worst | -13.586869600160133 | -4.7978427139200015 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].liquidation_shortfall | 0.47340000000000587 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].max_abs_inventory | 10.674299999999466 | 10.738600000000059 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].max_drawdown | 214.92608013190747 | 77.45454026368304 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].net_bp_per_notional | -0.8428525024682607 | -0.8292555753124956 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].net_per_hour | -9.548370180765978 | -3.0921486296159535 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].net_per_hour_over_inc_std | -4.235396918097953 | -2.943218053520913 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].orders_per_fill | 0.5553889136212359 | 0.829736032109569 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].own_edge_bp | 0.19930856860061913 | 0.22032414562290992 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].own_markout_1s_bp | -1.331051867638967 | -1.3935078643926393 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].own_markout_30s_bp | -1.6357913108456585 | -1.6518621827994977 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].own_markout_5s_bp | -1.5380061407839118 | -1.5860229110536408 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].paced_spells | 6982.4 | 1374.6 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].paced_time_share | 0.02126824938655596 | 0.004025750772733658 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].quote_presence_ask | 0.8572718446907912 | 0.8833023237180173 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].quote_presence_bid | 0.8613925164941927 | 0.9124113342498255 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].quote_presence_both | 0.7430465754652315 | 0.8036821947063014 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].turnover_per_hour | 111710.5368038879 | 38092.34496771199 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].tw_abs_inventory_avg | 5.653451631472341 | 5.617832556616072 |
| descriptive.scenarios[P3F/conservative/distant/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P3F/conservative/distant/vip0].gate_active_share | 1.0 | 1.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/conservative/distant/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/conservative/distant/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P3F/conservative/distant/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P3F/conservative/distant/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P3F/conservative/distant/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P3F/conservative/distant/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P3F/conservative/distant/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P3F/conservative/distant/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3F/conservative/distant/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip9].fill_rate | 0.015423663083997702 | 0.010657039940861677 |
| descriptive.scenarios[P3F/conservative/distant/vip9].gate_active_share | 0.9701859375803055 | 0.9830471098608635 |
| descriptive.scenarios[P3F/conservative/distant/vip9].gross_bp_per_notional | -2.8555352972947317 | -1.1788867982860831 |
| descriptive.scenarios[P3F/conservative/distant/vip9].gross_per_hour | -0.48057172313293756 | -0.21708113262551804 |
| descriptive.scenarios[P3F/conservative/distant/vip9].inc_es | 4.606386971202521 | 2.3384074507226513 |
| descriptive.scenarios[P3F/conservative/distant/vip9].inc_std | 1.8704515249240523 | 0.8609317032371215 |
| descriptive.scenarios[P3F/conservative/distant/vip9].inc_worst | -8.065948358180979 | -4.564847530740059 |
| descriptive.scenarios[P3F/conservative/distant/vip9].liquidation_shortfall | 0.1317000000000001 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip9].max_abs_inventory | 10.154299999999981 | 10.093800000000012 |
| descriptive.scenarios[P3F/conservative/distant/vip9].max_drawdown | 49.99581908845003 | 23.543390767079437 |
| descriptive.scenarios[P3F/conservative/distant/vip9].net_bp_per_notional | -4.047467203861603 | -2.440959051803752 |
| descriptive.scenarios[P3F/conservative/distant/vip9].net_per_hour | -0.9760717344543954 | -0.35921219947691513 |
| descriptive.scenarios[P3F/conservative/distant/vip9].net_per_hour_over_inc_std | -0.4989246986522458 | -0.32767908141947955 |
| descriptive.scenarios[P3F/conservative/distant/vip9].orders_per_fill | 12.21527014682839 | 17.712200517540488 |
| descriptive.scenarios[P3F/conservative/distant/vip9].own_edge_bp | 0.32846951065567165 | 0.29666718423086125 |
| descriptive.scenarios[P3F/conservative/distant/vip9].own_markout_1s_bp | -1.7851219086410453 | -1.7986485317225427 |
| descriptive.scenarios[P3F/conservative/distant/vip9].own_markout_30s_bp | -1.6336518765950387 | -1.8545356781038767 |
| descriptive.scenarios[P3F/conservative/distant/vip9].own_markout_5s_bp | -1.927404593466075 | -1.8788795081319936 |
| descriptive.scenarios[P3F/conservative/distant/vip9].paced_spells | 357.2 | 72.0 |
| descriptive.scenarios[P3F/conservative/distant/vip9].paced_time_share | 0.00041380667648351744 | 9.18298252441864e-05 |
| descriptive.scenarios[P3F/conservative/distant/vip9].quote_presence_ask | 0.12624069044390623 | 0.11688515768382776 |
| descriptive.scenarios[P3F/conservative/distant/vip9].quote_presence_bid | 0.11409142187336137 | 0.11872949068560171 |
| descriptive.scenarios[P3F/conservative/distant/vip9].quote_presence_both | 1.1816811056205211e-06 | 0.0 |
| descriptive.scenarios[P3F/conservative/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3F/conservative/distant/vip9].turnover_per_hour | 4321.585000241388 | 1169.0653961409703 |
| descriptive.scenarios[P3F/conservative/distant/vip9].tw_abs_inventory_avg | 5.758501319330401 | 3.801567910352169 |
| descriptive.scenarios[P3F/conservative/distant/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].fill_rate | 0.2826812566151199 | 0.23964370235381813 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].gate_active_share | 0.011385027432722582 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].gross_bp_per_notional | -1.6563572833635836 | -1.657996846999256 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].gross_per_hour | -22.36315657667516 | -6.757839805301094 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].inc_es | 6.578732089990258 | 3.1852070903359193 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].inc_std | 2.016564474838331 | 1.0115952308811131 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].inc_worst | -12.702551705040296 | -4.87121892991995 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].liquidation_shortfall | 0.4520000000000062 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].max_abs_inventory | 10.800100000000175 | 10.59280000000005 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].max_drawdown | 261.55744991969306 | 86.92014193420327 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].net_bp_per_notional | -0.8586339016571506 | -0.8646093563766513 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].net_per_hour | -11.725359156624652 | -3.4978462496356357 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].net_per_hour_over_inc_std | -5.007787209132511 | -3.210472399212815 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].orders_per_fill | 0.5043383538405628 | 0.8189529220183553 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].own_edge_bp | 0.17148185173405706 | 0.24654770181355215 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].own_markout_1s_bp | -1.3930014536136184 | -1.436123974710812 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].own_markout_30s_bp | -1.6669176284745215 | -1.686695056499638 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].own_markout_5s_bp | -1.5874729275511024 | -1.625497323626141 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].paced_spells | 7429.5 | 1374.0 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].paced_time_share | 0.022666399511447284 | 0.004010367813103111 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].quote_presence_ask | 0.8672916040385361 | 0.8791243394130659 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].quote_presence_bid | 0.87321202881638 | 0.9132219859146178 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].quote_presence_both | 0.7616938452018812 | 0.7987040879655136 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].turnover_per_hour | 133356.27517991472 | 40987.90014810428 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].tw_abs_inventory_avg | 5.692733865948609 | 5.660653883341705 |
| descriptive.scenarios[P3F/conservative/regional/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P3F/conservative/regional/vip0].gate_active_share | 1.0 | 1.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/conservative/regional/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/conservative/regional/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P3F/conservative/regional/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P3F/conservative/regional/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P3F/conservative/regional/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P3F/conservative/regional/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P3F/conservative/regional/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P3F/conservative/regional/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3F/conservative/regional/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip9].fill_rate | 0.012178675327023224 | 0.008571913526424486 |
| descriptive.scenarios[P3F/conservative/regional/vip9].gate_active_share | 0.9741942938652283 | 0.987596327667217 |
| descriptive.scenarios[P3F/conservative/regional/vip9].gross_bp_per_notional | -3.678630453222919 | -0.46960211102818433 |
| descriptive.scenarios[P3F/conservative/regional/vip9].gross_per_hour | -0.702829303694461 | -0.18033584005906655 |
| descriptive.scenarios[P3F/conservative/regional/vip9].inc_es | 5.007322443440158 | 2.084518420777338 |
| descriptive.scenarios[P3F/conservative/regional/vip9].inc_std | 1.876758705480596 | 0.7832293333921809 |
| descriptive.scenarios[P3F/conservative/regional/vip9].inc_worst | -9.173714172108664 | -4.084254019480258 |
| descriptive.scenarios[P3F/conservative/regional/vip9].liquidation_shortfall | 0.5218000000000004 | 0.0 |
| descriptive.scenarios[P3F/conservative/regional/vip9].max_abs_inventory | 10.0313 | 9.781600000000001 |
| descriptive.scenarios[P3F/conservative/regional/vip9].max_drawdown | 52.676370420479145 | 21.71818991206043 |
| descriptive.scenarios[P3F/conservative/regional/vip9].net_bp_per_notional | -4.869789381254708 | -1.772075745493891 |
| descriptive.scenarios[P3F/conservative/regional/vip9].net_per_hour | -1.0634539333356716 | -0.2987048686509731 |
| descriptive.scenarios[P3F/conservative/regional/vip9].net_per_hour_over_inc_std | -0.54902379272725 | -0.22047128327402304 |
| descriptive.scenarios[P3F/conservative/regional/vip9].orders_per_fill | 18.580890432654286 | 26.805653102103285 |
| descriptive.scenarios[P3F/conservative/regional/vip9].own_edge_bp | 0.2201164749964065 | 0.2694404471651511 |
| descriptive.scenarios[P3F/conservative/regional/vip9].own_markout_1s_bp | -2.1293020006146923 | -1.9467545152351462 |
| descriptive.scenarios[P3F/conservative/regional/vip9].own_markout_30s_bp | -2.068809490232847 | -1.8399345090279298 |
| descriptive.scenarios[P3F/conservative/regional/vip9].own_markout_5s_bp | -2.157055118431326 | -2.171290139724494 |
| descriptive.scenarios[P3F/conservative/regional/vip9].paced_spells | 381.0 | 95.0 |
| descriptive.scenarios[P3F/conservative/regional/vip9].paced_time_share | 0.000436121262393079 | 0.00012631266772852298 |
| descriptive.scenarios[P3F/conservative/regional/vip9].quote_presence_ask | 0.13305916370851498 | 0.11896350795331209 |
| descriptive.scenarios[P3F/conservative/regional/vip9].quote_presence_bid | 0.11733939664234667 | 0.1208639634868431 |
| descriptive.scenarios[P3F/conservative/regional/vip9].quote_presence_both | 2.4961789983659942e-06 | 7.989644202081127e-07 |
| descriptive.scenarios[P3F/conservative/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3F/conservative/regional/vip9].turnover_per_hour | 3147.462467252444 | 954.9693214577914 |
| descriptive.scenarios[P3F/conservative/regional/vip9].tw_abs_inventory_avg | 5.507624673623298 | 3.700558200326897 |
| descriptive.scenarios[P3F/conservative/regional/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].fill_rate | 0.28769737549311986 | 0.22078798577810507 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].gate_active_share | 0.01287106964510129 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].gross_bp_per_notional | -1.8562261368550577 | -1.904243084424635 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].gross_per_hour | -27.05547358400658 | -7.730059594273532 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].inc_es | 6.783784683280663 | 3.3527148700159266 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].inc_std | 2.0569780209593884 | 1.051235020676009 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].inc_worst | -11.615036495042318 | -5.300795465280677 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].liquidation_shortfall | 0.4606000000000073 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].max_abs_inventory | 10.445000000000316 | 10.050000000000107 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].max_drawdown | 337.91574525277605 | 108.27473648159844 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].net_bp_per_notional | -1.0581705899958938 | -1.110203354462983 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].net_per_hour | -15.239857703095032 | -4.431743662730415 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].net_per_hour_over_inc_std | -6.586536748717476 | -3.9408762374832165 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].orders_per_fill | 0.4959040330435446 | 0.8814507851724456 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].own_edge_bp | 0.34451017043392623 | 0.5110631906892608 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].own_markout_1s_bp | -1.6319909054357489 | -1.6436441018164771 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].own_markout_30s_bp | -1.8994553014982913 | -1.8737684398375716 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].own_markout_5s_bp | -1.8182006650016937 | -1.8160049647129461 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].paced_spells | 7715.9 | 1507.6 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].paced_time_share | 0.02357530469015536 | 0.00442417753256222 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].quote_presence_ask | 0.8625188419423442 | 0.8879938526814286 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].quote_presence_bid | 0.8456346905152046 | 0.8972839934926752 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].quote_presence_both | 0.7286587773184802 | 0.7913771526963507 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].turnover_per_hour | 148095.5714932834 | 41432.31594190108 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].tw_abs_inventory_avg | 5.9583627491771765 | 5.777174240699835 |
| descriptive.scenarios[P3F/conservative/tokyo/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].gate_active_share | 1.0 | 1.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].fill_rate | 0.01445799816594851 | 0.009526768933541666 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].gate_active_share | 0.9674232903973223 | 0.9770075356639051 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].gross_bp_per_notional | -1.4696512666995183 | -4.085460015301339 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].gross_per_hour | -0.9699091227196606 | -0.5086561104648105 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].inc_es | 5.348169549569077 | 2.4136371668293264 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].inc_std | 1.9964455580396236 | 0.9092017143490766 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].inc_worst | -9.994205335439158 | -4.683122860000067 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].liquidation_shortfall | 0.0035000000000001475 | 0.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].max_abs_inventory | 9.9852 | 9.911599999999993 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].max_drawdown | 58.42242386960969 | 28.53650929646036 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].net_bp_per_notional | -2.622749972997468 | -5.352375361911919 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].net_per_hour | -1.3682696964084147 | -0.6342281726747159 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].net_per_hour_over_inc_std | -0.553376405092323 | -0.5892301181738382 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].orders_per_fill | 18.54418400143564 | 30.475273255321053 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].own_edge_bp | 0.38962368254977575 | 0.47754310023078544 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].own_markout_1s_bp | -3.041291969542134 | -2.5541619781709755 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].own_markout_30s_bp | -2.977092006100084 | -3.5138134894386375 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].own_markout_5s_bp | -3.0340959491612844 | -3.298581527683595 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].paced_spells | 438.5 | 86.0 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].paced_time_share | 0.000491823207408184 | 0.00011383476123062971 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].quote_presence_ask | 0.12470445573957487 | 0.11485975900254095 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].quote_presence_bid | 0.11643055880476612 | 0.11303496658560216 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].quote_presence_both | 1.9760365842837606e-06 | 1.4124571215340359e-06 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].turnover_per_hour | 3479.107173715941 | 1034.9406485217473 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].tw_abs_inventory_avg | 5.671888036784913 | 4.482600008906752 |
| descriptive.scenarios[P3F/conservative/tokyo/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].fill_rate | 0.3351571917538879 | 0.3118787259989175 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].gate_active_share | 0.0133452073083134 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].gross_bp_per_notional | -1.450045505177117 | -1.4322496989631763 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].gross_per_hour | -19.232465813777797 | -6.697626618885302 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].inc_es | 6.1321298800550155 | 2.991350472799983 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].inc_std | 1.9437371784553512 | 0.968213003812977 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].inc_worst | -13.711519014960128 | -4.710584223680278 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].liquidation_shortfall | 0.5001000000000024 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].max_abs_inventory | 10.58909999999943 | 10.753400000000108 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].max_drawdown | 199.83192924570488 | 74.75740248603833 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].net_bp_per_notional | -0.6520889232875121 | -0.6369049211300364 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].net_per_hour | -8.86604928653149 | -2.893664618850791 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].net_per_hour_over_inc_std | -3.927017671070991 | -2.8416690329348677 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].orders_per_fill | 0.6106250574613786 | 0.888764759788536 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].own_edge_bp | 0.2741259861515585 | 0.3533713594499914 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].own_markout_1s_bp | -1.1168891978264734 | -1.1177922721219933 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].own_markout_30s_bp | -1.4346891216203452 | -1.3920268440834773 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].own_markout_5s_bp | -1.3217795845887172 | -1.3228684955138137 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].paced_spells | 7417.3 | 1598.0 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].paced_time_share | 0.0225395542085863 | 0.004664621966617389 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].quote_presence_ask | 0.8481088511779769 | 0.8891020196229802 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].quote_presence_bid | 0.8693008903951573 | 0.8922956917905406 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].quote_presence_both | 0.7428009106466293 | 0.79022811445471 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].turnover_per_hour | 129941.11643375964 | 47750.20895024877 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].tw_abs_inventory_avg | 5.446177735657146 | 5.570991992141417 |
| descriptive.scenarios[P3F/intermediate/distant/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P3F/intermediate/distant/vip0].gate_active_share | 1.0 | 1.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/intermediate/distant/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/intermediate/distant/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P3F/intermediate/distant/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P3F/intermediate/distant/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P3F/intermediate/distant/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P3F/intermediate/distant/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P3F/intermediate/distant/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P3F/intermediate/distant/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].fill_rate | 0.015701769840157812 | 0.011061916199698731 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].gate_active_share | 0.9691836146570715 | 0.9839475301178761 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].gross_bp_per_notional | -2.683712612489787 | -1.6100737790651702 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].gross_per_hour | -0.419612077279168 | -0.24155208929077188 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].inc_es | 4.589836867685884 | 2.3290717343346548 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].inc_std | 1.8737664037971407 | 0.8554807858519131 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].inc_worst | -7.804801888489625 | -4.4973883807402135 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].liquidation_shortfall | 0.19300000000000012 | 0.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].max_abs_inventory | 10.111099999999999 | 9.974000000000009 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].max_drawdown | 48.61685399629921 | 24.041424512738747 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].net_bp_per_notional | -3.8700200103297626 | -2.862912870016632 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].net_per_hour | -0.9200885124409336 | -0.38688373439935886 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].net_per_hour_over_inc_std | -0.481247346429862 | -0.37322592855203607 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].orders_per_fill | 12.17110658682989 | 18.031545427180255 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].own_edge_bp | 0.33468075141649206 | 0.31367676796839367 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].own_markout_1s_bp | -1.7669980921545823 | -1.7354448675111773 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].own_markout_30s_bp | -1.6655075291303068 | -1.8111183493577176 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].own_markout_5s_bp | -1.9075906610890445 | -1.8364247695839324 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].paced_spells | 359.6 | 72.0 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].paced_time_share | 0.00041621684224528097 | 9.182982524418637e-05 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].quote_presence_ask | 0.1239703061296437 | 0.11742456464433189 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].quote_presence_bid | 0.1144845668887543 | 0.11858790303473121 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].quote_presence_both | 1.1816811056205211e-06 | 1.5638124246464774e-08 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].turnover_per_hour | 4367.113653004042 | 1199.1117433381637 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].tw_abs_inventory_avg | 5.8659718323238765 | 3.8401357592702565 |
| descriptive.scenarios[P3F/intermediate/distant/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].fill_rate | 0.3377395720401301 | 0.30256289210734033 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].gate_active_share | 0.011160936029119857 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].gross_bp_per_notional | -1.5072700805714254 | -1.4330080502894866 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].gross_per_hour | -24.68158238722966 | -7.701392778650965 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].inc_es | 6.533436344485219 | 3.165202266303666 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].inc_std | 2.0196196353602556 | 0.9976080930804792 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].inc_worst | -12.579103469960796 | -4.977537540799746 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].liquidation_shortfall | 0.49960000000000004 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].max_abs_inventory | 10.796100000000331 | 10.754000000000017 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].max_drawdown | 263.1564461101259 | 84.16699075263982 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].net_bp_per_notional | -0.708955888176632 | -0.6373953300092753 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].net_per_hour | -11.754724725329382 | -3.3535883963404145 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].net_per_hour_over_inc_std | -5.0735984860844665 | -3.170642495405804 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].orders_per_fill | 0.5208665576082403 | 0.8146066418163931 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].own_edge_bp | 0.23016964499374729 | 0.34244483305412293 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].own_markout_1s_bp | -1.1812635320667744 | -1.1663852891053672 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].own_markout_30s_bp | -1.472503402131839 | -1.430623272880284 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].own_markout_5s_bp | -1.3732837943111733 | -1.3658665144869295 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].paced_spells | 8097.4 | 1678.2 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].paced_time_share | 0.02455619125783002 | 0.004917302495383665 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].quote_presence_ask | 0.8665437580323306 | 0.8931723502917684 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].quote_presence_bid | 0.8849408611701952 | 0.9053593777282364 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].quote_presence_both | 0.7732112829806034 | 0.8055197431950052 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].turnover_per_hour | 161958.30375993947 | 54556.616994223186 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].tw_abs_inventory_avg | 5.458957495710097 | 5.539076138269047 |
| descriptive.scenarios[P3F/intermediate/regional/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P3F/intermediate/regional/vip0].gate_active_share | 1.0 | 1.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/intermediate/regional/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/intermediate/regional/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P3F/intermediate/regional/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P3F/intermediate/regional/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P3F/intermediate/regional/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P3F/intermediate/regional/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P3F/intermediate/regional/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P3F/intermediate/regional/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].fill_rate | 0.012518711462386891 | 0.009031124664351117 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].gate_active_share | 0.9739953687528589 | 0.9882966581886521 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].gross_bp_per_notional | -3.3986491517557917 | -1.0584055205855136 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].gross_per_hour | -0.7069136556737384 | -0.21140097417735423 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].inc_es | 4.97758752434755 | 2.1304264411360023 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].inc_std | 1.8558606352240552 | 0.7984854515207745 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].inc_worst | -8.948004219559454 | -4.131986921080291 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].liquidation_shortfall | 0.4591999999999999 | 0.0 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].max_abs_inventory | 10.000300000000008 | 9.805200000000003 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].max_drawdown | 51.36161248146864 | 22.856042874280654 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].net_bp_per_notional | -4.583091179896319 | -2.3560262148995994 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].net_per_hour | -1.074755825801735 | -0.3342378729554569 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].net_per_hour_over_inc_std | -0.5615778056829146 | -0.2775986656717432 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].orders_per_fill | 18.697913028014376 | 26.994331599521445 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].own_edge_bp | 0.22870456536355382 | 0.2898823220104447 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].own_markout_1s_bp | -2.0981116499568957 | -1.9040978670309658 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].own_markout_30s_bp | -2.0312554646800063 | -1.8000912302356558 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].own_markout_5s_bp | -2.126261314552539 | -2.124823952318933 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].paced_spells | 378.8 | 92.4 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].paced_time_share | 0.0004326931914549607 | 0.00012225094967493214 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].quote_presence_ask | 0.131495885431341 | 0.11871998087989111 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].quote_presence_bid | 0.11720717958377971 | 0.12154915177162537 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].quote_presence_both | 2.4961789983659942e-06 | 7.989644202081127e-07 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].turnover_per_hour | 3216.5169772799104 | 992.0552245672673 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].tw_abs_inventory_avg | 5.489973189760467 | 3.7545595063682944 |
| descriptive.scenarios[P3F/intermediate/regional/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].fill_rate | 0.3427540384063868 | 0.2848840195331811 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].gate_active_share | 0.012984804435575165 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].gross_bp_per_notional | -1.6806365906081762 | -1.599647653644731 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].gross_per_hour | -30.540158214969438 | -9.080399597026949 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].inc_es | 6.80570532574159 | 3.276827824106624 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].inc_std | 2.0353111135682735 | 1.0274886353864476 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].inc_worst | -11.689200082239145 | -5.42025194543993 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].liquidation_shortfall | 0.4611000000000011 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].max_abs_inventory | 10.316900000000377 | 10.154399999999985 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].max_drawdown | 352.8963103881818 | 109.2695994753445 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].net_bp_per_notional | -0.8821883465186048 | -0.8041749822622763 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].net_per_hour | -15.883679134561367 | -4.495346858963405 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].net_per_hour_over_inc_std | -6.988017998546949 | -4.121179150856451 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].orders_per_fill | 0.48573159030862884 | 0.8142030085674467 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].own_edge_bp | 0.3600185957254259 | 0.529596838703723 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].own_markout_1s_bp | -1.3898071646486487 | -1.3379913189443795 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].own_markout_30s_bp | -1.669742619053422 | -1.5816345585276437 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].own_markout_5s_bp | -1.5773488535404863 | -1.5302672886510897 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].paced_spells | 8488.9 | 1815.2 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].paced_time_share | 0.02571962959696513 | 0.005333052419671683 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].quote_presence_ask | 0.8666010079770963 | 0.8998936770308618 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].quote_presence_bid | 0.8623022110151679 | 0.8987139113826432 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].quote_presence_both | 0.7501125860068905 | 0.8051538178219223 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].turnover_per_hour | 183623.3069967117 | 57543.35347204444 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].tw_abs_inventory_avg | 5.729273245861415 | 5.5404743277782895 |
| descriptive.scenarios[P3F/intermediate/tokyo/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].gate_active_share | 1.0 | 1.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].fill_rate | 0.014655252434775352 | 0.009892522310440657 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].gate_active_share | 0.965976880130853 | 0.9771349930563824 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].gross_bp_per_notional | -1.5503292133986284 | -4.799409468642208 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].gross_per_hour | -1.012446012358622 | -0.5506830297356329 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].inc_es | 5.338616834502064 | 2.426155734424009 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].inc_std | 2.001764758971861 | 0.9053850607074226 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].inc_worst | -10.008276378159094 | -4.75535360000005 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].liquidation_shortfall | 0.10350000000000034 | 0.0 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].max_abs_inventory | 9.950200000000004 | 9.923799999999996 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].max_drawdown | 59.025989118349855 | 29.186546671400272 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].net_bp_per_notional | -2.7047198520582065 | -6.055824945493592 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].net_per_hour | -1.4152044255429472 | -0.6794369206082291 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].net_per_hour_over_inc_std | -0.5814805887617462 | -0.6503709326267743 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].orders_per_fill | 18.43043476967396 | 29.90575642747341 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].own_edge_bp | 0.3904627014737796 | 0.4780106350866604 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].own_markout_1s_bp | -3.0012600923442463 | -2.4995403747452904 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].own_markout_30s_bp | -2.9807644200264947 | -3.3549600315946244 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].own_markout_5s_bp | -2.994428297322565 | -3.1927956318840227 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].paced_spells | 436.7 | 86.2 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].paced_time_share | 0.0004897289339205103 | 0.00011406612164276376 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].quote_presence_ask | 0.12259646766038039 | 0.1148753991459516 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].quote_presence_bid | 0.1167316241860488 | 0.11346135609733768 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].quote_presence_both | 2.0816786129130175e-06 | 1.4124571215340359e-06 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].turnover_per_hour | 3513.1311546687693 | 1060.1955382738863 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].tw_abs_inventory_avg | 5.681469596941199 | 4.380948426602552 |
| descriptive.scenarios[P3F/intermediate/tokyo/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].fill_rate | 0.4717429118625092 | 0.49649121111536 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].gate_active_share | 0.01028402659744671 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].gross_bp_per_notional | -1.113320679099135 | -0.9826941350561793 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].gross_per_hour | -21.306545463979994 | -8.07720331545124 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].inc_es | 5.6821490328165 | 2.7567999343466743 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].inc_std | 1.912504772467227 | 0.9446565912637379 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].inc_worst | -12.951043210078447 | -4.775215343199562 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].liquidation_shortfall | 0.45589999999999903 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].max_abs_inventory | 10.424899999999967 | 9.998600000000046 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].max_drawdown | 153.87510934653704 | 45.735682805539376 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].net_bp_per_notional | -0.3146740644782466 | -0.1849597613648738 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].net_per_hour | -6.620405962816202 | -1.555081758774306 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].net_per_hour_over_inc_std | -2.8157327148565807 | -1.5511919431119647 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].orders_per_fill | 0.5475415935382482 | 0.7254367517150577 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].own_edge_bp | 0.4173535830045497 | 0.58020707924803 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].own_markout_1s_bp | -0.7814025765053354 | -0.72786394829674 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].own_markout_30s_bp | -1.079723695312139 | -0.996439327963721 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].own_markout_5s_bp | -0.9755574810734814 | -0.934525540532323 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].paced_spells | 9540.0 | 2379.0 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].paced_time_share | 0.028726942150871564 | 0.006995925645094476 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].quote_presence_ask | 0.8176300793548039 | 0.8777091148189285 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].quote_presence_bid | 0.8582122459126158 | 0.8767012860933983 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].quote_presence_both | 0.7079497254032214 | 0.7662979812905195 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].turnover_per_hour | 183936.9464037752 | 81717.26713571126 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].tw_abs_inventory_avg | 5.4289108453968735 | 5.435717613705192 |
| descriptive.scenarios[P3F/optimistic/distant/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P3F/optimistic/distant/vip0].gate_active_share | 1.0 | 1.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/optimistic/distant/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/optimistic/distant/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P3F/optimistic/distant/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P3F/optimistic/distant/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P3F/optimistic/distant/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P3F/optimistic/distant/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P3F/optimistic/distant/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P3F/optimistic/distant/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].fill_rate | 0.024329101085963013 | 0.02061650653124427 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].gate_active_share | 0.967471721765903 | 0.9826574980393932 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].gross_bp_per_notional | -2.7295415696340646 | -1.906057282132392 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].gross_per_hour | -0.9423471305019515 | -0.2973758278571124 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].inc_es | 4.936413702111432 | 2.46784400633064 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].inc_std | 1.9772083930396829 | 0.9137780710652119 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].inc_worst | -10.489504274079724 | -4.427801675040109 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].liquidation_shortfall | 0.4691999999999997 | 0.0 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].max_abs_inventory | 10.266299999999998 | 9.832600000000005 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].max_drawdown | 63.71807780473898 | 27.042046955619632 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].net_bp_per_notional | -3.896166534430448 | -3.1129053577804635 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].net_per_hour | -1.678648710064794 | -0.5656028519432896 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].net_per_hour_over_inc_std | -0.8010013672402442 | -0.6623969588972717 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].orders_per_fill | 12.094072051453509 | 19.561426327670485 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].own_edge_bp | 0.5261400471650117 | 0.6411948490690031 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].own_markout_1s_bp | -1.4090509394746467 | -1.2731192235917317 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].own_markout_30s_bp | -1.366862218083401 | -1.465377138589171 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].own_markout_5s_bp | -1.5535093030050948 | -1.3864864395367686 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].paced_spells | 334.6 | 75.2 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].paced_time_share | 0.0003869658209259343 | 9.682227915066121e-05 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].quote_presence_ask | 0.11907981004266524 | 0.11296432794975457 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].quote_presence_bid | 0.11316952554630491 | 0.11600387259762408 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].quote_presence_both | 1.3275345883591764e-06 | 1.9724214775379759e-07 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].turnover_per_hour | 6480.720775573916 | 2287.6886421055938 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].tw_abs_inventory_avg | 6.280447706721837 | 4.495305650609512 |
| descriptive.scenarios[P3F/optimistic/distant/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].fill_rate | 0.5599122310001163 | 0.5758097353288768 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].gate_active_share | 0.00833313533964321 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].gross_bp_per_notional | -1.180195518580213 | -1.0660452759633867 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].gross_per_hour | -32.578267032915 | -12.207125693118297 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].inc_es | 6.4135364929313905 | 3.066922209770686 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].inc_std | 2.0087255264138486 | 0.9967210858313683 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].inc_worst | -12.783559670002216 | -5.607239037598797 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].liquidation_shortfall | 0.5414999999999998 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].max_abs_inventory | 10.41080000000024 | 10.101800000000036 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].max_drawdown | 249.12305561914772 | 82.91162370244385 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].net_bp_per_notional | -0.381278066143317 | -0.2681945513837668 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].net_per_hour | -11.169995185526423 | -3.1851974219524237 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].net_per_hour_over_inc_std | -4.738645512594912 | -2.952430000909633 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].orders_per_fill | 0.47866184471310974 | 0.6462385003026053 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].own_edge_bp | 0.41211027687668594 | 0.5775235450960421 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].own_markout_1s_bp | -0.8693800086480552 | -0.8210300730939478 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].own_markout_30s_bp | -1.150408305312239 | -1.068052682442539 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].own_markout_5s_bp | -1.0558628602276445 | -1.0200767599382865 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].paced_spells | 12287.7 | 3103.2 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].paced_time_share | 0.0365744236477207 | 0.00916191508410794 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].quote_presence_ask | 0.8321282519885399 | 0.8916090340852565 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].quote_presence_bid | 0.8710398234524023 | 0.8889481695408925 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].quote_presence_both | 0.7330717333737757 | 0.7902982030916842 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].turnover_per_hour | 268016.17308970646 | 112981.54434763291 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].tw_abs_inventory_avg | 5.421171182331777 | 5.396513483568827 |
| descriptive.scenarios[P3F/optimistic/regional/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P3F/optimistic/regional/vip0].gate_active_share | 1.0 | 1.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/optimistic/regional/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/optimistic/regional/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P3F/optimistic/regional/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P3F/optimistic/regional/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P3F/optimistic/regional/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P3F/optimistic/regional/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P3F/optimistic/regional/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P3F/optimistic/regional/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].fill_rate | 0.017203527338009457 | 0.014902527431258302 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].gate_active_share | 0.9729528146668246 | 0.9872081603747551 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].gross_bp_per_notional | -2.239380872683063 | -1.9010549766002849 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].gross_per_hour | -0.6691548208115617 | -0.16671289477061793 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].inc_es | 4.930187133950897 | 2.351555371937315 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].inc_std | 1.884983407755725 | 0.9095221292372413 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].inc_worst | -9.0786813876795 | -4.436287003900016 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].liquidation_shortfall | 0.5305 | 0.0 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].max_abs_inventory | 10.196000000000002 | 9.914600000000004 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].max_drawdown | 48.27709386726261 | 24.32749068965895 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].net_bp_per_notional | -3.397547174292311 | -3.121468497758726 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].net_per_hour | -1.1546398088397694 | -0.35843194483691676 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].net_per_hour_over_inc_std | -0.5602472631513316 | -0.3911237944061664 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].orders_per_fill | 18.894727055390156 | 27.199861918778225 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].own_edge_bp | 0.46126386904486844 | 0.6076558304647645 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].own_markout_1s_bp | -1.727626780978012 | -1.4676415338711901 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].own_markout_30s_bp | -1.6197822039844236 | -1.439633174053073 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].own_markout_5s_bp | -1.753507620768905 | -1.6235259001375286 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].paced_spells | 409.7 | 97.2 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].paced_time_share | 0.00044721292386899834 | 0.00012304928620497264 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].quote_presence_ask | 0.12616089678736955 | 0.11847709539407514 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].quote_presence_bid | 0.11796469665184592 | 0.11831510743350368 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].quote_presence_both | 2.1471287896126296e-06 | 5.148279967014671e-07 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].turnover_per_hour | 4271.393427767059 | 1604.3132830806148 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].tw_abs_inventory_avg | 5.82558863498925 | 4.448936694198599 |
| descriptive.scenarios[P3F/optimistic/regional/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].fill_rate | 0.6062742203874171 | 0.6212136092577694 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].gate_active_share | 0.008954830262056282 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].gross_bp_per_notional | -1.3718592526799793 | -1.2584853119672768 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].gross_per_hour | -45.596458202961855 | -17.580109550100836 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].inc_es | 7.141338873343905 | 3.600489951648202 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].inc_std | 2.06132348714224 | 1.0897166244976206 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].inc_worst | -12.766717407800774 | -5.968184922720221 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].liquidation_shortfall | 0.4471999999999978 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].max_abs_inventory | 10.09530000000071 | 10.000000000000007 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].max_drawdown | 426.7102271409876 | 159.4193891463517 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].net_bp_per_notional | -0.5727676913951143 | -0.4602007075296145 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].net_per_hour | -19.31582074212438 | -6.509623792064465 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].net_per_hour_over_inc_std | -8.362884180445668 | -5.528995683450077 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].orders_per_fill | 0.38563413407053065 | 0.5175438025639467 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].own_edge_bp | 0.4112053981991031 | 0.577103522634536 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].own_markout_1s_bp | -1.0624032600953728 | -1.0021909471448036 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].own_markout_30s_bp | -1.3481882300095678 | -1.234988322000801 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].own_markout_5s_bp | -1.2491482144166217 | -1.1954941605195002 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].paced_spells | 11221.9 | 2619.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].paced_time_share | 0.03346336855049623 | 0.007628925517931344 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].quote_presence_ask | 0.8437980093464503 | 0.8923450643363555 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].quote_presence_bid | 0.8648219646184512 | 0.8924372388409738 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].quote_presence_both | 0.7344462398162449 | 0.7925254349062524 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].turnover_per_hour | 328927.4203635043 | 138593.34635375426 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].tw_abs_inventory_avg | 5.546414823385513 | 5.404682570311978 |
| descriptive.scenarios[P3F/optimistic/tokyo/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].gate_active_share | 1.0 | 1.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].fill_rate | 0.022625353322872313 | 0.018488274488105458 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].gate_active_share | 0.9636828894608096 | 0.9805885483331911 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].gross_bp_per_notional | -1.509997379257952 | -2.950550906301073 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].gross_per_hour | -1.2618731196978472 | -0.48420544636517204 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].inc_es | 5.416831793176106 | 2.5759647463040047 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].inc_std | 1.9988773245776923 | 0.9415042853271304 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].inc_worst | -10.833154728010204 | -5.167343874600234 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].liquidation_shortfall | 0.4638999999999996 | 0.0 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].max_abs_inventory | 9.983800000000006 | 9.860599999999994 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].max_drawdown | 62.397474757520854 | 33.846380680979955 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].net_bp_per_notional | -2.644963075516982 | -4.129724754541607 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].net_per_hour | -1.8610672222200215 | -0.7133691779291 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].net_per_hour_over_inc_std | -0.7972448552281287 | -0.7436299156066545 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].orders_per_fill | 16.399389624473088 | 25.07086443516522 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].own_edge_bp | 0.4372481319715263 | 0.5929341273234809 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].own_markout_1s_bp | -2.4060909116789015 | -1.9021891357052827 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].own_markout_30s_bp | -2.357923899828147 | -2.2946335620907403 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].own_markout_5s_bp | -2.3836186351696735 | -2.348059670448341 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].paced_spells | 469.9 | 107.8 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].paced_time_share | 0.000504895609387481 | 0.0001411319134255377 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].quote_presence_ask | 0.12044037841400276 | 0.11404180844342113 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].quote_presence_bid | 0.11509160120729253 | 0.11317455145650401 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].quote_presence_both | 2.133026502270635e-06 | 1.3649002594304353e-06 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].turnover_per_hour | 5285.036625477436 | 1965.1108809171124 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].tw_abs_inventory_avg | 5.9144961664325395 | 4.55446934186547 |
| descriptive.scenarios[P3F/optimistic/tokyo/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].fill_rate | 0.10306237610567068 | 0.12961397740679265 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].gate_active_share | 0.5258789515199307 | 0.2390054538217036 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].gross_bp_per_notional | -1.6231211515791142 | -1.6102035265554722 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].gross_per_hour | -6.466073678248913 | -3.2668404111133293 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].inc_es | 5.597586365094233 | 2.844267766559991 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].inc_std | 2.0632499951560783 | 0.9872278948196964 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].inc_worst | -11.421936839920798 | -5.105378029119392 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].max_abs_inventory | 10.51929999999978 | 10.339399999999994 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].max_drawdown | 93.01672837410857 | 47.934099744199855 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].net_bp_per_notional | -0.8300823250252659 | -0.8234714950172976 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].net_per_hour | -3.3777579763147805 | -1.698535546957168 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].net_per_hour_over_inc_std | -1.5166559006698013 | -1.6368679321118922 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].orders_per_fill | 1.2844542384828352 | 1.4282092168655314 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].own_edge_bp | 0.19309267557042423 | 0.1735631454759242 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].own_markout_1s_bp | -1.5785626103769395 | -1.5737504008757752 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].own_markout_30s_bp | -1.7754404871548455 | -1.7763740865619666 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].own_markout_5s_bp | -1.7467458185470957 | -1.7386180504430313 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].paced_spells | 4577.4 | 1273.4 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].paced_time_share | 0.009277073282184054 | 0.0026596834227283245 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].quote_presence_ask | 0.596383063643225 | 0.7668865864691774 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].quote_presence_bid | 0.6195911415291638 | 0.8175439454902816 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].quote_presence_both | 0.31098197193544624 | 0.6154944321076791 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].turnover_per_hour | 38904.53875986485 | 19858.152582578678 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].tw_abs_inventory_avg | 6.353381373780872 | 5.7194551798434405 |
| descriptive.scenarios[P3_M1/conservative/distant/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].fill_rate | 0.10306237610567068 | 0.12961397740679265 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].gate_active_share | 0.5258789515199307 | 0.2390054538217036 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].gross_bp_per_notional | -1.6231211515791142 | -1.6102035265554722 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].gross_per_hour | -6.466073678248913 | -3.2668404111133293 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].inc_es | 13.454811705063912 | 7.318567515333385 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].inc_std | 3.4522328029833127 | 1.809540501373116 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].inc_worst | -21.155203274000677 | -13.12781634999888 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].max_abs_inventory | 10.51929999999978 | 10.339399999999994 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].max_drawdown | 1019.4017324339131 | 555.9144790040028 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].net_bp_per_notional | -11.653387123084125 | -11.667890345954714 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].net_per_hour | -45.475166346179236 | -23.213459699996935 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].net_per_hour_over_inc_std | -12.217901191202504 | -12.109208429598976 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].orders_per_fill | 1.2844542384828352 | 1.4282092168655314 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].own_edge_bp | 0.19309267557042423 | 0.1735631454759242 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].own_markout_1s_bp | -1.5785626103769395 | -1.5737504008757752 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].own_markout_30s_bp | -1.7754404871548455 | -1.7763740865619666 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].own_markout_5s_bp | -1.7467458185470957 | -1.7386180504430313 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].paced_spells | 4577.4 | 1273.4 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].paced_time_share | 0.009277073282184054 | 0.0026596834227283245 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].quote_presence_ask | 0.596383063643225 | 0.7668865864691774 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].quote_presence_bid | 0.6195911415291638 | 0.8175439454902816 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].quote_presence_both | 0.31098197193544624 | 0.6154944321076791 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].turnover_per_hour | 38904.53875986485 | 19858.152582578678 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].tw_abs_inventory_avg | 6.353381373780872 | 5.7194551798434405 |
| descriptive.scenarios[P3_M1/conservative/distant/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].fill_rate | 0.10306237610567068 | 0.12961397740679265 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].gate_active_share | 0.5258789515199307 | 0.2390054538217036 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].gross_bp_per_notional | -1.6231211515791142 | -1.6102035265554722 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].gross_per_hour | -6.466073678248913 | -3.2668404111133293 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].inc_es | 6.727202962785154 | 3.492071309526706 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].inc_std | 2.1664813454028238 | 1.0482529101665259 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].inc_worst | -13.081675556960903 | -6.474323209959297 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].max_abs_inventory | 10.51929999999978 | 10.339399999999994 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].max_drawdown | 247.2687026477438 | 133.03579557616064 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].net_bp_per_notional | -2.730082325025266 | -2.723471495017298 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].net_per_hour | -10.769620340689105 | -5.471584537647116 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].net_per_hour_over_inc_std | -4.582919513161498 | -4.9636327276123735 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].orders_per_fill | 1.2844542384828352 | 1.4282092168655314 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].own_edge_bp | 0.19309267557042423 | 0.1735631454759242 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].own_markout_1s_bp | -1.5785626103769395 | -1.5737504008757752 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].own_markout_30s_bp | -1.7754404871548455 | -1.7763740865619666 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].own_markout_5s_bp | -1.7467458185470957 | -1.7386180504430313 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].paced_spells | 4577.4 | 1273.4 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].paced_time_share | 0.009277073282184054 | 0.0026596834227283245 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].quote_presence_ask | 0.596383063643225 | 0.7668865864691774 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].quote_presence_bid | 0.6195911415291638 | 0.8175439454902816 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].quote_presence_both | 0.31098197193544624 | 0.6154944321076791 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].turnover_per_hour | 38904.53875986485 | 19858.152582578678 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].tw_abs_inventory_avg | 6.353381373780872 | 5.7194551798434405 |
| descriptive.scenarios[P3_M1/conservative/distant/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].fill_rate | 0.08613648557240158 | 0.1081648400239134 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].gate_active_share | 0.5161242385904089 | 0.22866346971642662 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].gross_bp_per_notional | -1.7211433237172333 | -1.76501226340982 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].gross_per_hour | -5.58439419398577 | -3.147830238517553 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].inc_es | 5.43685118135849 | 3.0041189317119477 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].inc_std | 1.9839354469624073 | 1.024585348096652 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].inc_worst | -11.023107308559245 | -5.519078828959559 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].max_abs_inventory | 10.522100000000032 | 10.556399999999986 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].max_drawdown | 86.70692161840226 | 50.756096655718714 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].net_bp_per_notional | -0.9306675312108444 | -0.9777271550058637 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].net_per_hour | -3.071291167712303 | -1.829845458063792 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].net_per_hour_over_inc_std | -1.4483631903943823 | -1.6681547941373054 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].orders_per_fill | 1.7397959517610242 | 1.8500364606521054 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].own_edge_bp | 0.15768770917273164 | 0.2057808536598648 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].own_markout_1s_bp | -1.7564603447233147 | -1.6616876576663724 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].own_markout_30s_bp | -2.0003712133652543 | -1.791611595653428 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].own_markout_5s_bp | -1.9278144447133094 | -1.8198192450983854 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].paced_spells | 4916.3 | 1270.2 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].paced_time_share | 0.009732710408498216 | 0.0026324495062444173 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].quote_presence_ask | 0.6027508411368732 | 0.7654382951557226 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].quote_presence_bid | 0.6220940554533761 | 0.8151181601089462 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].quote_presence_both | 0.3163541857640049 | 0.6146796886718249 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].turnover_per_hour | 31738.42252495168 | 16681.363754924037 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].tw_abs_inventory_avg | 6.290763619341954 | 5.794209807394358 |
| descriptive.scenarios[P3_M1/conservative/regional/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].fill_rate | 0.08613648557240158 | 0.1081648400239134 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].gate_active_share | 0.5161242385904089 | 0.22866346971642662 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].gross_bp_per_notional | -1.7211433237172333 | -1.76501226340982 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].gross_per_hour | -5.58439419398577 | -3.147830238517553 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].inc_es | 13.375349178132746 | 7.0751599355998325 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].inc_std | 3.4344838356376775 | 1.7561020141314863 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].inc_worst | -22.821962583999753 | -12.648870169999949 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].max_abs_inventory | 10.522100000000032 | 10.556399999999986 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].max_drawdown | 843.5424887129608 | 476.6659993919954 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].net_bp_per_notional | -11.762552921515542 | -11.820294400783924 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].net_per_hour | -37.43573313512296 | -19.90103886274664 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].net_per_hour_over_inc_std | -10.31114369232887 | -10.734278791047561 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].orders_per_fill | 1.7397959517610242 | 1.8500364606521054 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].own_edge_bp | 0.15768770917273164 | 0.2057808536598648 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].own_markout_1s_bp | -1.7564603447233147 | -1.6616876576663724 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].own_markout_30s_bp | -2.0003712133652543 | -1.791611595653428 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].own_markout_5s_bp | -1.9278144447133094 | -1.8198192450983854 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].paced_spells | 4916.3 | 1270.2 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].paced_time_share | 0.009732710408498216 | 0.0026324495062444173 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].quote_presence_ask | 0.6027508411368732 | 0.7654382951557226 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].quote_presence_bid | 0.6220940554533761 | 0.8151181601089462 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].quote_presence_both | 0.3163541857640049 | 0.6146796886718249 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].turnover_per_hour | 31738.42252495168 | 16681.363754924037 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].tw_abs_inventory_avg | 6.290763619341954 | 5.794209807394358 |
| descriptive.scenarios[P3_M1/conservative/regional/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].fill_rate | 0.08613648557240158 | 0.1081648400239134 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].gate_active_share | 0.5161242385904089 | 0.22866346971642662 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].gross_bp_per_notional | -1.7211433237172333 | -1.76501226340982 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].gross_per_hour | -5.58439419398577 | -3.147830238517553 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].inc_es | 6.551035225484642 | 3.5795680979279227 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].inc_std | 2.115511347482306 | 1.0889786750874664 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].inc_worst | -12.664906377688737 | -6.6047036101795085 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].max_abs_inventory | 10.522100000000032 | 10.556399999999986 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].max_drawdown | 211.16395089841367 | 121.35771596901706 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].net_bp_per_notional | -2.8306675312108447 | -2.877727155005864 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].net_per_hour | -9.10159144745312 | -4.999304571499359 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].net_per_hour_over_inc_std | -4.054977100115898 | -4.3836702162829235 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].orders_per_fill | 1.7397959517610242 | 1.8500364606521054 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].own_edge_bp | 0.15768770917273164 | 0.2057808536598648 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].own_markout_1s_bp | -1.7564603447233147 | -1.6616876576663724 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].own_markout_30s_bp | -2.0003712133652543 | -1.791611595653428 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].own_markout_5s_bp | -1.9278144447133094 | -1.8198192450983854 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].paced_spells | 4916.3 | 1270.2 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].paced_time_share | 0.009732710408498216 | 0.0026324495062444173 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].quote_presence_ask | 0.6027508411368732 | 0.7654382951557226 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].quote_presence_bid | 0.6220940554533761 | 0.8151181601089462 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].quote_presence_both | 0.3163541857640049 | 0.6146796886718249 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].turnover_per_hour | 31738.42252495168 | 16681.363754924037 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].tw_abs_inventory_avg | 6.290763619341954 | 5.794209807394358 |
| descriptive.scenarios[P3_M1/conservative/regional/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].fill_rate | 0.08663336147674179 | 0.09420816257504824 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].gate_active_share | 0.5029765005110469 | 0.2205449874794855 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].gross_bp_per_notional | -2.2116599568646125 | -2.251521010666333 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].gross_per_hour | -6.848257533341885 | -3.4859635131332505 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].inc_es | 5.768435826558752 | 3.018044188405384 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].inc_std | 2.05281235290211 | 1.0485106397552308 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].inc_worst | -10.748166679998992 | -5.2525272072004245 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].max_abs_inventory | 10.004099999999944 | 9.9896 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].max_drawdown | 113.31189296273581 | 60.304853653942835 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].net_bp_per_notional | -1.4194988682745477 | -1.4663678576282377 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].net_per_hour | -4.3981103031339055 | -2.3092623052501957 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].net_per_hour_over_inc_std | -2.1788797477897672 | -2.1249350545779775 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].orders_per_fill | 2.0087352904868667 | 2.4014807534755573 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].own_edge_bp | 0.3454864904810312 | 0.48572150948376425 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].own_markout_1s_bp | -2.256348131614059 | -2.0682928887772385 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].own_markout_30s_bp | -2.579353767735785 | -2.186946584060755 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].own_markout_5s_bp | -2.4243534532341866 | -2.227491204902729 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].paced_spells | 4924.5 | 1411.8 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].paced_time_share | 0.009825400496354551 | 0.0029375738213093536 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].quote_presence_ask | 0.60120577617887 | 0.76371761669492 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].quote_presence_bid | 0.6023647773892165 | 0.793463283963229 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].quote_presence_both | 0.3031746355356179 | 0.5924642351579247 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].turnover_per_hour | 30933.65906073349 | 14926.630700373868 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].tw_abs_inventory_avg | 6.205324354993355 | 6.025127559876685 |
| descriptive.scenarios[P3_M1/conservative/tokyo/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].fill_rate | 0.08663336147674179 | 0.09420816257504824 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].gate_active_share | 0.5029765005110469 | 0.2205449874794855 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].gross_bp_per_notional | -2.2116599568646125 | -2.251521010666333 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].gross_per_hour | -6.848257533341885 | -3.4859635131332505 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].inc_es | 13.10198875351222 | 6.700353814533292 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].inc_std | 3.4483518274218037 | 1.7209136574910804 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].inc_worst | -22.540529692999314 | -11.555977850000605 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].max_abs_inventory | 10.004099999999944 | 9.9896 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].max_drawdown | 853.4357623549716 | 442.8123781160014 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].net_bp_per_notional | -12.245742180386072 | -12.316072519196355 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].net_per_hour | -37.88863613603495 | -18.488373553276055 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].net_per_hour_over_inc_std | -10.38065311316264 | -10.16300838604712 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].orders_per_fill | 2.0087352904868667 | 2.4014807534755573 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].own_edge_bp | 0.3454864904810312 | 0.48572150948376425 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].own_markout_1s_bp | -2.256348131614059 | -2.0682928887772385 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].own_markout_30s_bp | -2.579353767735785 | -2.186946584060755 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].own_markout_5s_bp | -2.4243534532341866 | -2.227491204902729 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].paced_spells | 4924.5 | 1411.8 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].paced_time_share | 0.009825400496354551 | 0.0029375738213093536 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].quote_presence_ask | 0.60120577617887 | 0.76371761669492 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].quote_presence_bid | 0.6023647773892165 | 0.793463283963229 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].quote_presence_both | 0.3031746355356179 | 0.5924642351579247 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].turnover_per_hour | 30933.65906073349 | 14926.630700373868 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].tw_abs_inventory_avg | 6.205324354993355 | 6.025127559876685 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].fill_rate | 0.08663336147674179 | 0.09420816257504824 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].gate_active_share | 0.5029765005110469 | 0.2205449874794855 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].gross_bp_per_notional | -2.2116599568646125 | -2.251521010666333 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].gross_per_hour | -6.848257533341885 | -3.4859635131332505 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].inc_es | 6.800674267081592 | 3.584739506868007 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].inc_std | 2.178835692193581 | 1.1179322561584595 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].inc_worst | -12.429665837647772 | -6.0660717081608535 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].max_abs_inventory | 10.004099999999944 | 9.9896 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].max_drawdown | 239.00431029506643 | 124.59875687102267 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].net_bp_per_notional | -3.319498868274548 | -3.366367857628238 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].net_per_hour | -10.27550552467327 | -5.145322138321231 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].net_per_hour_over_inc_std | -4.6236694553453965 | -4.400770728282445 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].orders_per_fill | 2.0087352904868667 | 2.4014807534755573 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].own_edge_bp | 0.3454864904810312 | 0.48572150948376425 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].own_markout_1s_bp | -2.256348131614059 | -2.0682928887772385 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].own_markout_30s_bp | -2.579353767735785 | -2.186946584060755 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].own_markout_5s_bp | -2.4243534532341866 | -2.227491204902729 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].paced_spells | 4924.5 | 1411.8 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].paced_time_share | 0.009825400496354551 | 0.0029375738213093536 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].quote_presence_ask | 0.60120577617887 | 0.76371761669492 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].quote_presence_bid | 0.6023647773892165 | 0.793463283963229 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].quote_presence_both | 0.3031746355356179 | 0.5924642351579247 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].turnover_per_hour | 30933.65906073349 | 14926.630700373868 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].tw_abs_inventory_avg | 6.205324354993355 | 6.025127559876685 |
| descriptive.scenarios[P3_M1/conservative/tokyo/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].fill_rate | 0.11684059090430998 | 0.15815732272617122 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].gate_active_share | 0.5207083263429253 | 0.2400430672247913 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].gross_bp_per_notional | -1.4707051100483732 | -1.4788890386705318 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].gross_per_hour | -6.60969930306852 | -3.5572190306689024 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].inc_es | 5.692950905858291 | 2.8635424638292593 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].inc_std | 2.11903565050066 | 0.9815416672904996 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].inc_worst | -12.004694568160518 | -4.600055340799702 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].max_abs_inventory | 10.477799999999794 | 10.435000000000006 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].max_drawdown | 90.20983174608804 | 45.777429510326314 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].net_bp_per_notional | -0.676982575337133 | -0.687836461039881 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].net_per_hour | -3.2297115407164947 | -1.6566520702787355 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].net_per_hour_over_inc_std | -1.3851611534050432 | -1.6379618294217368 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].orders_per_fill | 1.339496848682933 | 1.4997600095704275 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].own_edge_bp | 0.24299176215978294 | 0.28633412086552773 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].own_markout_1s_bp | -1.4243539376132168 | -1.341659736616158 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].own_markout_30s_bp | -1.632488986664748 | -1.5314559324201737 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].own_markout_5s_bp | -1.5954095828660602 | -1.5116970826248566 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].paced_spells | 4568.4 | 1316.4 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].paced_time_share | 0.009213706461462825 | 0.002764480966749125 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].quote_presence_ask | 0.5800426627872998 | 0.7770921586706107 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].quote_presence_bid | 0.6244992519103348 | 0.8080991356895566 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].quote_presence_both | 0.30435093723136186 | 0.61347997788964 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].turnover_per_hour | 42563.93959731689 | 23973.20950865471 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].tw_abs_inventory_avg | 6.438266740575668 | 5.655591946824275 |
| descriptive.scenarios[P3_M1/intermediate/distant/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].fill_rate | 0.11684059090430998 | 0.15815732272617122 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].gate_active_share | 0.5207083263429253 | 0.2400430672247913 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].gross_bp_per_notional | -1.4707051100483732 | -1.4788890386705318 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].gross_per_hour | -6.60969930306852 | -3.5572190306689024 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].inc_es | 13.929303275660539 | 7.913225960666582 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].inc_std | 3.5144349160972177 | 1.880173244642019 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].inc_worst | -22.083047220998694 | -13.37543076399923 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].max_abs_inventory | 10.477799999999794 | 10.435000000000006 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].max_drawdown | 1105.1717481189137 | 661.0867909220077 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].net_bp_per_notional | -11.497998437390809 | -11.517790875059008 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].net_per_hour | -49.28288848922596 | -27.605601584115828 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].net_per_hour_over_inc_std | -13.258291580339227 | -13.937915944078137 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].orders_per_fill | 1.339496848682933 | 1.4997600095704275 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].own_edge_bp | 0.24299176215978294 | 0.28633412086552773 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].own_markout_1s_bp | -1.4243539376132168 | -1.341659736616158 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].own_markout_30s_bp | -1.632488986664748 | -1.5314559324201737 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].own_markout_5s_bp | -1.5954095828660602 | -1.5116970826248566 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].paced_spells | 4568.4 | 1316.4 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].paced_time_share | 0.009213706461462825 | 0.002764480966749125 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].quote_presence_ask | 0.5800426627872998 | 0.7770921586706107 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].quote_presence_bid | 0.6244992519103348 | 0.8080991356895566 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].quote_presence_both | 0.30435093723136186 | 0.61347997788964 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].turnover_per_hour | 42563.93959731689 | 23973.20950865471 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].tw_abs_inventory_avg | 6.438266740575668 | 5.655591946824275 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].fill_rate | 0.11684059090430998 | 0.15815732272617122 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].gate_active_share | 0.5207083263429253 | 0.2400430672247913 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].gross_bp_per_notional | -1.4707051100483732 | -1.4788890386705318 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].gross_per_hour | -6.60969930306852 | -3.5572190306689024 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].inc_es | 6.908346277424231 | 3.577384031778606 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].inc_std | 2.2150089956900088 | 1.0456189045891138 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].inc_worst | -13.747243235450773 | -5.867540643839693 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].max_abs_inventory | 10.477799999999794 | 10.435000000000006 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].max_drawdown | 258.9413558702303 | 149.2032393941248 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].net_bp_per_notional | -2.576982575337133 | -2.5878364610398807 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].net_per_hour | -11.316860064206704 | -6.21156187692313 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].net_per_hour_over_inc_std | -4.754478385737838 | -5.663658326041132 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].orders_per_fill | 1.339496848682933 | 1.4997600095704275 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].own_edge_bp | 0.24299176215978294 | 0.28633412086552773 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].own_markout_1s_bp | -1.4243539376132168 | -1.341659736616158 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].own_markout_30s_bp | -1.632488986664748 | -1.5314559324201737 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].own_markout_5s_bp | -1.5954095828660602 | -1.5116970826248566 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].paced_spells | 4568.4 | 1316.4 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].paced_time_share | 0.009213706461462825 | 0.002764480966749125 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].quote_presence_ask | 0.5800426627872998 | 0.7770921586706107 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].quote_presence_bid | 0.6244992519103348 | 0.8080991356895566 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].quote_presence_both | 0.30435093723136186 | 0.61347997788964 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].turnover_per_hour | 42563.93959731689 | 23973.20950865471 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].tw_abs_inventory_avg | 6.438266740575668 | 5.655591946824275 |
| descriptive.scenarios[P3_M1/intermediate/distant/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].fill_rate | 0.10047151684928161 | 0.13704819794451548 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].gate_active_share | 0.5088416266123204 | 0.23145471614502844 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].gross_bp_per_notional | -1.6324374358434273 | -1.5341353159775106 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].gross_per_hour | -6.192127136281203 | -3.374704650189264 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].inc_es | 5.639173488913991 | 2.871123460778513 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].inc_std | 2.0382818254709854 | 1.0025089434761498 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].inc_worst | -11.146559116800097 | -5.376326273600353 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].max_abs_inventory | 10.478200000000047 | 10.809000000000033 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].max_drawdown | 88.86503930618076 | 46.1203979677592 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].net_bp_per_notional | -0.8397886232184074 | -0.7457726436046919 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].net_per_hour | -3.3505098098593087 | -1.6933498976359964 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].net_per_hour_over_inc_std | -1.5221126149443607 | -1.621939545418193 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].orders_per_fill | 1.767773288323546 | 1.85368976930931 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].own_edge_bp | 0.20325827283894554 | 0.295603300335223 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].own_markout_1s_bp | -1.559842387294837 | -1.4009462956050842 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].own_markout_30s_bp | -1.811673288450192 | -1.5537543466433288 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].own_markout_5s_bp | -1.7275529301228272 | -1.5631928356896392 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].paced_spells | 4927.9 | 1308.2 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].paced_time_share | 0.009756278914545679 | 0.0027112638922555847 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].quote_presence_ask | 0.5827896492444764 | 0.7723676319956587 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].quote_presence_bid | 0.6271846889068177 | 0.8092408517345075 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].quote_presence_both | 0.3105390226193621 | 0.6107082679317422 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].turnover_per_hour | 35805.1659629927 | 21254.887431235966 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].tw_abs_inventory_avg | 6.439183627997268 | 5.779741683274648 |
| descriptive.scenarios[P3_M1/intermediate/regional/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].fill_rate | 0.10047151684928161 | 0.13704819794451548 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].gate_active_share | 0.5088416266123204 | 0.23145471614502844 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].gross_bp_per_notional | -1.6324374358434273 | -1.5341353159775106 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].gross_per_hour | -6.192127136281203 | -3.374704650189264 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].inc_es | 14.031749452332832 | 7.853034065199712 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].inc_std | 3.552288924856697 | 1.8653122364597994 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].inc_worst | -23.33241258700046 | -13.248916717998958 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].max_abs_inventory | 10.478200000000047 | 10.809000000000033 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].max_drawdown | 948.7858109429674 | 591.8157869500014 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].net_bp_per_notional | -11.664399120082473 | -11.584732392617429 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].net_per_hour | -42.09640592804574 | -24.712358350753966 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].net_per_hour_over_inc_std | -11.373430764023878 | -12.653356794462548 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].orders_per_fill | 1.767773288323546 | 1.85368976930931 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].own_edge_bp | 0.20325827283894554 | 0.295603300335223 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].own_markout_1s_bp | -1.559842387294837 | -1.4009462956050842 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].own_markout_30s_bp | -1.811673288450192 | -1.5537543466433288 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].own_markout_5s_bp | -1.7275529301228272 | -1.5631928356896392 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].paced_spells | 4927.9 | 1308.2 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].paced_time_share | 0.009756278914545679 | 0.0027112638922555847 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].quote_presence_ask | 0.5827896492444764 | 0.7723676319956587 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].quote_presence_bid | 0.6271846889068177 | 0.8092408517345075 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].quote_presence_both | 0.3105390226193621 | 0.6107082679317422 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].turnover_per_hour | 35805.1659629927 | 21254.887431235966 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].tw_abs_inventory_avg | 6.439183627997268 | 5.779741683274648 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].fill_rate | 0.10047151684928161 | 0.13704819794451548 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].gate_active_share | 0.5088416266123204 | 0.23145471614502844 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].gross_bp_per_notional | -1.6324374358434273 | -1.5341353159775106 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].gross_per_hour | -6.192127136281203 | -3.374704650189264 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].inc_es | 6.808698442804163 | 3.5981824344731947 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].inc_std | 2.17368335217468 | 1.0755327106367425 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].inc_worst | -12.959849530470294 | -6.520403496579746 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].max_abs_inventory | 10.478200000000047 | 10.809000000000033 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].max_drawdown | 233.53168132749957 | 137.90814098037805 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].net_bp_per_notional | -2.739788623218408 | -2.645772643604692 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].net_per_hour | -10.153491342827923 | -5.73177850957083 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].net_per_hour_over_inc_std | -4.42404125233549 | -5.106792192754632 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].orders_per_fill | 1.767773288323546 | 1.85368976930931 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].own_edge_bp | 0.20325827283894554 | 0.295603300335223 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].own_markout_1s_bp | -1.559842387294837 | -1.4009462956050842 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].own_markout_30s_bp | -1.811673288450192 | -1.5537543466433288 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].own_markout_5s_bp | -1.7275529301228272 | -1.5631928356896392 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].paced_spells | 4927.9 | 1308.2 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].paced_time_share | 0.009756278914545679 | 0.0027112638922555847 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].quote_presence_ask | 0.5827896492444764 | 0.7723676319956587 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].quote_presence_bid | 0.6271846889068177 | 0.8092408517345075 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].quote_presence_both | 0.3105390226193621 | 0.6107082679317422 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].turnover_per_hour | 35805.1659629927 | 21254.887431235966 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].tw_abs_inventory_avg | 6.439183627997268 | 5.779741683274648 |
| descriptive.scenarios[P3_M1/intermediate/regional/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].fill_rate | 0.0997641685518229 | 0.12192235142437872 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].gate_active_share | 0.4999768023573111 | 0.2232460804022252 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].gross_bp_per_notional | -2.050505900838705 | -1.829609372707754 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].gross_per_hour | -7.398490869394751 | -3.5776642265413585 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].inc_es | 5.888609340086895 | 2.871985284714575 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].inc_std | 2.090684796181887 | 1.0189045371411958 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].inc_worst | -11.081236097919378 | -5.091497801759835 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].max_abs_inventory | 9.992500000000083 | 9.996400000000019 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].max_drawdown | 117.2595454472616 | 55.1772099935376 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].net_bp_per_notional | -1.257105699917213 | -1.0429694744448263 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].net_per_hour | -4.649450856468354 | -2.073484880043405 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].net_per_hour_over_inc_std | -2.179298226909288 | -1.9928321871310044 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].orders_per_fill | 1.9381249891639385 | 2.258165129348235 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].own_edge_bp | 0.3559774565488956 | 0.5051333006993455 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].own_markout_1s_bp | -2.006945346867762 | -1.7504861117764015 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].own_markout_30s_bp | -2.334056587743333 | -1.862933385648676 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].own_markout_5s_bp | -2.1695266952857972 | -1.8978203079339822 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].paced_spells | 4929.5 | 1430.8 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].paced_time_share | 0.009815844896045525 | 0.002990199523488029 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].quote_presence_ask | 0.5843041523535233 | 0.7696794213951378 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].quote_presence_bid | 0.6101036016329477 | 0.7966426488143694 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].quote_presence_both | 0.3006013632903041 | 0.5991743542016128 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].turnover_per_hour | 34651.86544270038 | 19063.312829621078 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].tw_abs_inventory_avg | 6.32839550496948 | 5.8966241388903455 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].fill_rate | 0.0997641685518229 | 0.12192235142437872 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].gate_active_share | 0.4999768023573111 | 0.2232460804022252 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].gross_bp_per_notional | -2.050505900838705 | -1.829609372707754 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].gross_per_hour | -7.398490869394751 | -3.5776642265413585 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].inc_es | 13.787027010765224 | 7.227042183999769 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].inc_std | 3.5545354982053654 | 1.7919663053877755 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].inc_worst | -23.147141675998885 | -11.844789491999913 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].max_abs_inventory | 9.992500000000083 | 9.996400000000019 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].max_drawdown | 949.3562252719869 | 544.4048210039965 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].net_bp_per_notional | -12.079200679440914 | -11.887696771564592 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].net_per_hour | -42.150831192484844 | -22.731784359952577 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].net_per_hour_over_inc_std | -11.30734669292038 | -12.155742641158243 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].orders_per_fill | 1.9381249891639385 | 2.258165129348235 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].own_edge_bp | 0.3559774565488956 | 0.5051333006993455 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].own_markout_1s_bp | -2.006945346867762 | -1.7504861117764015 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].own_markout_30s_bp | -2.334056587743333 | -1.862933385648676 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].own_markout_5s_bp | -2.1695266952857972 | -1.8978203079339822 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].paced_spells | 4929.5 | 1430.8 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].paced_time_share | 0.009815844896045525 | 0.002990199523488029 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].quote_presence_ask | 0.5843041523535233 | 0.7696794213951378 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].quote_presence_bid | 0.6101036016329477 | 0.7966426488143694 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].quote_presence_both | 0.3006013632903041 | 0.5991743542016128 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].turnover_per_hour | 34651.86544270038 | 19063.312829621078 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].tw_abs_inventory_avg | 6.32839550496948 | 5.8966241388903455 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].fill_rate | 0.0997641685518229 | 0.12192235142437872 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].gate_active_share | 0.4999768023573111 | 0.2232460804022252 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].gross_bp_per_notional | -2.050505900838705 | -1.829609372707754 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].gross_per_hour | -7.398490869394751 | -3.5776642265413585 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].inc_es | 6.998200786775942 | 3.5359015794585473 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].inc_std | 2.2228480304323153 | 1.0937515895962526 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].inc_worst | -12.849897090358803 | -5.837321897579825 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].max_abs_inventory | 9.992500000000083 | 9.996400000000019 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].max_drawdown | 259.1697011199338 | 136.78368640385744 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].net_bp_per_notional | -3.1571056999172127 | -2.9429694744448263 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].net_per_hour | -11.233305290581425 | -5.695514317671409 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].net_per_hour_over_inc_std | -4.916812191256351 | -5.030310109821288 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].orders_per_fill | 1.9381249891639385 | 2.258165129348235 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].own_edge_bp | 0.3559774565488956 | 0.5051333006993455 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].own_markout_1s_bp | -2.006945346867762 | -1.7504861117764015 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].own_markout_30s_bp | -2.334056587743333 | -1.862933385648676 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].own_markout_5s_bp | -2.1695266952857972 | -1.8978203079339822 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].paced_spells | 4929.5 | 1430.8 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].paced_time_share | 0.009815844896045525 | 0.002990199523488029 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].quote_presence_ask | 0.5843041523535233 | 0.7696794213951378 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].quote_presence_bid | 0.6101036016329477 | 0.7966426488143694 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].quote_presence_both | 0.3006013632903041 | 0.5991743542016128 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].turnover_per_hour | 34651.86544270038 | 19063.312829621078 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].tw_abs_inventory_avg | 6.32839550496948 | 5.8966241388903455 |
| descriptive.scenarios[P3_M1/intermediate/tokyo/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].fill_rate | 0.1954730027602378 | 0.29821313017224976 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].gate_active_share | 0.5056549288996537 | 0.2365862986459099 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].gross_bp_per_notional | -1.152707093848384 | -0.9412612950312449 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].gross_per_hour | -8.740750309319798 | -4.544672265640036 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].inc_es | 5.724571052205906 | 2.8192156912533197 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].inc_std | 2.0977785314284882 | 1.027384601574337 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].inc_worst | -11.685208132321346 | -5.14892142560002 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].liquidation_shortfall | 0.25759999999999933 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].max_abs_inventory | 10.395200000000086 | 10.192399999999981 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].max_drawdown | 91.57346752674425 | 31.361093014075756 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].net_bp_per_notional | -0.3572309748141684 | -0.14487105294070107 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].net_per_hour | -3.323914741072963 | -0.6587984680821244 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].net_per_hour_over_inc_std | -1.349728365694275 | -0.6764012002455531 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].orders_per_fill | 1.2117078281761162 | 1.2469862784805423 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].own_edge_bp | 0.426778458960679 | 0.5822255912291437 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].own_markout_1s_bp | -0.9624273850401737 | -0.8139983031860802 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].own_markout_30s_bp | -1.1875881927127685 | -0.996761136864046 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].own_markout_5s_bp | -1.1258278745533152 | -0.9742660780104366 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].paced_spells | 5209.1 | 1761.8 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].paced_time_share | 0.010338656895128156 | 0.003642720195666408 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].quote_presence_ask | 0.5555135621375874 | 0.7727418712342434 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].quote_presence_bid | 0.6258523281566178 | 0.7893320457118019 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].quote_presence_both | 0.2924162733055674 | 0.5904283020979989 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].turnover_per_hour | 68056.46798644446 | 48772.33968751175 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].tw_abs_inventory_avg | 6.571069403503688 | 5.789146463857061 |
| descriptive.scenarios[P3_M1/optimistic/distant/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].fill_rate | 0.1954730027602378 | 0.29821313017224976 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].gate_active_share | 0.5056549288996537 | 0.2365862986459099 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].gross_bp_per_notional | -1.152707093848384 | -0.9412612950312449 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].gross_per_hour | -8.740750309319798 | -4.544672265640036 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].inc_es | 18.118537525623303 | 12.955596164666613 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].inc_std | 4.388746333170578 | 2.909583270208965 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].inc_worst | -25.783232832000557 | -19.67196608800071 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].liquidation_shortfall | 0.25759999999999933 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].max_abs_inventory | 10.395200000000086 | 10.192399999999981 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].max_drawdown | 1735.034758005951 | 1278.038263564013 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].net_bp_per_notional | -11.172376141525708 | -10.956955894637577 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].net_per_hour | -76.9175742551935 | -53.38620055073018 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].net_per_hour_over_inc_std | -16.837110564661913 | -17.487984134307162 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].orders_per_fill | 1.2117078281761162 | 1.2469862784805423 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].own_edge_bp | 0.426778458960679 | 0.5822255912291437 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].own_markout_1s_bp | -0.9624273850401737 | -0.8139983031860802 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].own_markout_30s_bp | -1.1875881927127685 | -0.996761136864046 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].own_markout_5s_bp | -1.1258278745533152 | -0.9742660780104366 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].paced_spells | 5209.1 | 1761.8 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].paced_time_share | 0.010338656895128156 | 0.003642720195666408 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].quote_presence_ask | 0.5555135621375874 | 0.7727418712342434 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].quote_presence_bid | 0.6258523281566178 | 0.7893320457118019 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].quote_presence_both | 0.2924162733055674 | 0.5904283020979989 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].turnover_per_hour | 68056.46798644446 | 48772.33968751175 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].tw_abs_inventory_avg | 6.571069403503688 | 5.789146463857061 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].fill_rate | 0.1954730027602378 | 0.29821313017224976 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].gate_active_share | 0.5056549288996537 | 0.2365862986459099 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].gross_bp_per_notional | -1.152707093848384 | -0.9412612950312449 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].gross_per_hour | -8.740750309319798 | -4.544672265640036 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].inc_es | 7.4868483647336985 | 4.236625486305295 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].inc_std | 2.2651050932917074 | 1.1657628357598329 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].inc_worst | -14.056299755561446 | -7.219163787840119 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].liquidation_shortfall | 0.25759999999999933 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].max_abs_inventory | 10.395200000000086 | 10.192399999999981 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].max_drawdown | 370.57860005332367 | 237.70353361063562 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].net_bp_per_notional | -2.2572309748141683 | -2.0448710529407013 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].net_per_hour | -16.25464365849741 | -9.925543008709358 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].net_per_hour_over_inc_std | -6.8448394182197685 | -8.137661053449593 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].orders_per_fill | 1.2117078281761162 | 1.2469862784805423 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].own_edge_bp | 0.426778458960679 | 0.5822255912291437 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].own_markout_1s_bp | -0.9624273850401737 | -0.8139983031860802 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].own_markout_30s_bp | -1.1875881927127685 | -0.996761136864046 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].own_markout_5s_bp | -1.1258278745533152 | -0.9742660780104366 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].paced_spells | 5209.1 | 1761.8 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].paced_time_share | 0.010338656895128156 | 0.003642720195666408 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].quote_presence_ask | 0.5555135621375874 | 0.7727418712342434 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].quote_presence_bid | 0.6258523281566178 | 0.7893320457118019 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].quote_presence_both | 0.2924162733055674 | 0.5904283020979989 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].turnover_per_hour | 68056.46798644446 | 48772.33968751175 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].tw_abs_inventory_avg | 6.571069403503688 | 5.789146463857061 |
| descriptive.scenarios[P3_M1/optimistic/distant/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].fill_rate | 0.17942559898474975 | 0.28408504236204624 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].gate_active_share | 0.4904198135109814 | 0.22418640276568502 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].gross_bp_per_notional | -1.1608100644726884 | -1.0015020607038545 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].gross_per_hour | -8.109988396935991 | -4.896918946856607 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].inc_es | 5.733937426029489 | 2.9798322428801054 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].inc_std | 2.098626753653468 | 1.05496862720181 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].inc_worst | -10.691886514479638 | -5.287521332960461 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].liquidation_shortfall | 0.33250000000000013 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].max_abs_inventory | 10.35079999999994 | 10.160400000000042 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].max_drawdown | 91.47993034520904 | 38.48857003767853 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].net_bp_per_notional | -0.36591097447710086 | -0.20582019767372967 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].net_per_hour | -3.239333682713108 | -1.06545244060447 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].net_per_hour_over_inc_std | -1.321687082610133 | -0.9791941879475508 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].orders_per_fill | 1.4662077342892483 | 1.346654305778721 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].own_edge_bp | 0.4157154117946158 | 0.5785373966175129 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].own_markout_1s_bp | -1.0345912096950372 | -0.8495903193390276 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].own_markout_30s_bp | -1.245407621779141 | -1.0247312093629375 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].own_markout_5s_bp | -1.1659081266206315 | -1.0055330126614008 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].paced_spells | 5924.2 | 1992.2 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].paced_time_share | 0.011181205719767 | 0.0040143146015039505 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].quote_presence_ask | 0.5536520597432042 | 0.7697695111189832 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].quote_presence_bid | 0.6290635533428661 | 0.79457111022776 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].quote_presence_both | 0.29988805073081987 | 0.5952949811261042 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].turnover_per_hour | 61224.40760055203 | 48117.300491850125 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].tw_abs_inventory_avg | 6.649238608021342 | 5.980194091694164 |
| descriptive.scenarios[P3_M1/optimistic/regional/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].fill_rate | 0.17942559898474975 | 0.28408504236204624 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].gate_active_share | 0.4904198135109814 | 0.22418640276568502 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].gross_bp_per_notional | -1.1608100644726884 | -1.0015020607038545 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].gross_per_hour | -8.109988396935991 | -4.896918946856607 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].inc_es | 18.70681747422637 | 13.895271945200008 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].inc_std | 4.514416021524045 | 3.093233392429352 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].inc_worst | -28.30793014900032 | -21.719001649999257 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].liquidation_shortfall | 0.33250000000000013 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].max_abs_inventory | 10.35079999999994 | 10.160400000000042 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].max_drawdown | 1572.881045980946 | 1271.0981975340142 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].net_bp_per_notional | -11.182987934057092 | -11.020276569268528 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].net_per_hour | -69.45308249236317 | -53.09212175651487 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].net_per_hour_over_inc_std | -14.930448849661696 | -16.38996143063713 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].orders_per_fill | 1.4662077342892483 | 1.346654305778721 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].own_edge_bp | 0.4157154117946158 | 0.5785373966175129 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].own_markout_1s_bp | -1.0345912096950372 | -0.8495903193390276 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].own_markout_30s_bp | -1.245407621779141 | -1.0247312093629375 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].own_markout_5s_bp | -1.1659081266206315 | -1.0055330126614008 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].paced_spells | 5924.2 | 1992.2 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].paced_time_share | 0.011181205719767 | 0.0040143146015039505 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].quote_presence_ask | 0.5536520597432042 | 0.7697695111189832 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].quote_presence_bid | 0.6290635533428661 | 0.79457111022776 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].quote_presence_both | 0.29988805073081987 | 0.5952949811261042 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].turnover_per_hour | 61224.40760055203 | 48117.300491850125 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].tw_abs_inventory_avg | 6.649238608021342 | 5.980194091694164 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].fill_rate | 0.17942559898474975 | 0.28408504236204624 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].gate_active_share | 0.4904198135109814 | 0.22418640276568502 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].gross_bp_per_notional | -1.1608100644726884 | -1.0015020607038545 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].gross_per_hour | -8.109988396935991 | -4.896918946856607 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].inc_es | 7.579724448242041 | 4.6136927017201135 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].inc_std | 2.3126604996854843 | 1.2486586837140212 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].inc_worst | -13.242121713920644 | -7.953696468139986 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].liquidation_shortfall | 0.33250000000000013 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].max_abs_inventory | 10.35079999999994 | 10.160400000000042 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].max_drawdown | 341.58787001912435 | 244.54779941855924 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].net_bp_per_notional | -2.2659109744771007 | -2.10582019767373 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].net_per_hour | -14.871971126817996 | -10.207739534055994 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].net_per_hour_over_inc_std | -6.245660419546629 | -7.789466919097007 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].orders_per_fill | 1.4662077342892483 | 1.346654305778721 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].own_edge_bp | 0.4157154117946158 | 0.5785373966175129 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].own_markout_1s_bp | -1.0345912096950372 | -0.8495903193390276 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].own_markout_30s_bp | -1.245407621779141 | -1.0247312093629375 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].own_markout_5s_bp | -1.1659081266206315 | -1.0055330126614008 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].paced_spells | 5924.2 | 1992.2 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].paced_time_share | 0.011181205719767 | 0.0040143146015039505 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].quote_presence_ask | 0.5536520597432042 | 0.7697695111189832 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].quote_presence_bid | 0.6290635533428661 | 0.79457111022776 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].quote_presence_both | 0.29988805073081987 | 0.5952949811261042 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].turnover_per_hour | 61224.40760055203 | 48117.300491850125 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].tw_abs_inventory_avg | 6.649238608021342 | 5.980194091694164 |
| descriptive.scenarios[P3_M1/optimistic/regional/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].fill_rate | 0.19889460609467485 | 0.3038175494837627 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].gate_active_share | 0.49282600279766625 | 0.22076101477447732 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].gross_bp_per_notional | -1.500293096742359 | -1.2262644897200219 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].gross_per_hour | -11.050394438446729 | -6.74092468198521 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].inc_es | 5.9679029656416205 | 3.08799008775468 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].inc_std | 2.102078584538264 | 1.0657289179146874 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].inc_worst | -11.322177571041934 | -5.248487126560743 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].max_abs_inventory | 9.998700000000044 | 9.995999999999992 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].max_drawdown | 137.24210383745415 | 65.45731612273694 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].net_bp_per_notional | -0.7041460579515064 | -0.43027235836019423 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].net_per_hour | -5.566860879972884 | -2.470763788774972 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].net_per_hour_over_inc_std | -2.513332674043833 | -2.208416664021182 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].orders_per_fill | 1.4607882481941517 | 1.3114763807060843 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].own_edge_bp | 0.413374346862328 | 0.5776597314037366 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].own_markout_1s_bp | -1.358823192737587 | -1.0778778045279274 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].own_markout_30s_bp | -1.593989244468355 | -1.2337072491257237 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].own_markout_5s_bp | -1.4951877758520693 | -1.2195120177819723 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].paced_spells | 5873.0 | 1681.2 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].paced_time_share | 0.011198562951720012 | 0.0034518936175817173 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].quote_presence_ask | 0.5684370058500813 | 0.7701561762033521 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].quote_presence_bid | 0.6241269559522461 | 0.8006458307011692 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].quote_presence_both | 0.3038801448497471 | 0.6027692884058765 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].turnover_per_hour | 68844.35986180657 | 53607.659084702944 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].tw_abs_inventory_avg | 6.341150981468062 | 5.856059933640221 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].fill_rate | 0.19889460609467485 | 0.3038175494837627 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].gate_active_share | 0.49282600279766625 | 0.22076101477447732 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].gross_bp_per_notional | -1.500293096742359 | -1.2262644897200219 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].gross_per_hour | -11.050394438446729 | -6.74092468198521 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].inc_es | 20.34766268007493 | 15.313118937333144 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].inc_std | 4.917180305747804 | 3.460238930132145 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].inc_worst | -30.465255367001067 | -22.709038608001446 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].max_abs_inventory | 9.998700000000044 | 9.995999999999992 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].max_drawdown | 1810.949240551985 | 1446.9537646380097 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].net_bp_per_notional | -11.517045101999523 | -11.243690005546858 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].net_per_hour | -79.999168345778 | -60.42880913001859 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].net_per_hour_over_inc_std | -15.60917100982106 | -16.716549141508427 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].orders_per_fill | 1.4607882481941517 | 1.3114763807060843 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].own_edge_bp | 0.413374346862328 | 0.5776597314037366 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].own_markout_1s_bp | -1.358823192737587 | -1.0778778045279274 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].own_markout_30s_bp | -1.593989244468355 | -1.2337072491257237 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].own_markout_5s_bp | -1.4951877758520693 | -1.2195120177819723 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].paced_spells | 5873.0 | 1681.2 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].paced_time_share | 0.011198562951720012 | 0.0034518936175817173 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].quote_presence_ask | 0.5684370058500813 | 0.7701561762033521 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].quote_presence_bid | 0.6241269559522461 | 0.8006458307011692 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].quote_presence_both | 0.3038801448497471 | 0.6027692884058765 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].turnover_per_hour | 68844.35986180657 | 53607.659084702944 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].tw_abs_inventory_avg | 6.341150981468062 | 5.856059933640221 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].fill_rate | 0.19889460609467485 | 0.3038175494837627 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].gate_active_share | 0.49282600279766625 | 0.22076101477447732 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].gross_bp_per_notional | -1.500293096742359 | -1.2262644897200219 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].gross_per_hour | -11.050394438446729 | -6.74092468198521 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].inc_es | 8.055510082640286 | 4.901376372810614 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].inc_std | 2.378534956818528 | 1.3244493569103102 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].inc_worst | -14.133374025431584 | -8.014866247600333 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].max_abs_inventory | 9.998700000000044 | 9.995999999999992 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].max_drawdown | 426.4458374609709 | 303.19636952791996 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].net_bp_per_notional | -2.6041460579515063 | -2.3302723583601948 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].net_per_hour | -18.64728925371613 | -12.656219014868535 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].net_per_hour_over_inc_std | -7.629722466413908 | -9.099290329072863 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].orders_per_fill | 1.4607882481941517 | 1.3114763807060843 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].own_edge_bp | 0.413374346862328 | 0.5776597314037366 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].own_markout_1s_bp | -1.358823192737587 | -1.0778778045279274 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].own_markout_30s_bp | -1.593989244468355 | -1.2337072491257237 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].own_markout_5s_bp | -1.4951877758520693 | -1.2195120177819723 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].paced_spells | 5873.0 | 1681.2 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].paced_time_share | 0.011198562951720012 | 0.0034518936175817173 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].quote_presence_ask | 0.5684370058500813 | 0.7701561762033521 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].quote_presence_bid | 0.6241269559522461 | 0.8006458307011692 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].quote_presence_both | 0.3038801448497471 | 0.6027692884058765 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].turnover_per_hour | 68844.35986180657 | 53607.659084702944 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].tw_abs_inventory_avg | 6.341150981468062 | 5.856059933640221 |
| descriptive.scenarios[P3_M1/optimistic/tokyo/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].fill_rate | 0.10348988097762027 | 0.13203404429564164 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].gate_active_share | 0.5140761299302854 | 0.23173997971877652 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].gross_bp_per_notional | -1.6939117548720266 | -1.5554078802549882 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].gross_per_hour | -6.707103806792469 | -3.222243212769102 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].inc_es | 5.626921518774184 | 2.8106229175892454 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].inc_std | 2.0674739956297774 | 0.982189461002456 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].inc_worst | -11.104866366160971 | -5.284522163839347 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].max_abs_inventory | 10.613600000000078 | 10.436800000000034 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].max_drawdown | 96.12057782693088 | 47.27735268669625 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].net_bp_per_notional | -0.9018989268982123 | -0.7679336062226606 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].net_per_hour | -3.6299672955249043 | -1.6365015353952326 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].net_per_hour_over_inc_std | -1.632623903829423 | -1.560095138331582 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].orders_per_fill | 1.2818247774365374 | 1.4121349007444646 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].own_edge_bp | 0.19366871542831335 | 0.17769037241798308 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].own_markout_1s_bp | -1.5728738008913108 | -1.5658171884482193 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].own_markout_30s_bp | -1.7909327203390948 | -1.7796848596319736 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].own_markout_5s_bp | -1.7572523686631087 | -1.7309809299512362 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].paced_spells | 4298.9 | 1164.8 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].paced_time_share | 0.0088720563459517 | 0.002465014151623335 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].quote_presence_ask | 0.5979688981432183 | 0.7784270625804248 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].quote_presence_bid | 0.622453180858349 | 0.8187162349500203 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].quote_presence_both | 0.31704518988751323 | 0.6266404291870611 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].turnover_per_hour | 38787.42725033309 | 20063.680153794332 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].tw_abs_inventory_avg | 6.391286316219372 | 5.69313523408167 |
| descriptive.scenarios[P3_M2/conservative/distant/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].fill_rate | 0.10348988097762027 | 0.13203404429564164 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].gate_active_share | 0.5140761299302854 | 0.23173997971877652 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].gross_bp_per_notional | -1.6939117548720266 | -1.5554078802549882 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].gross_per_hour | -6.707103806792469 | -3.222243212769102 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].inc_es | 13.444711982965776 | 7.293326081599952 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].inc_std | 3.4371701968401083 | 1.78468347189605 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].inc_worst | -20.837767773000817 | -13.040644323998922 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].max_abs_inventory | 10.613600000000078 | 10.436800000000034 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].max_drawdown | 1023.4015390069095 | 559.6499008119993 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].net_bp_per_notional | -11.728638589768487 | -11.609867558375303 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].net_per_hour | -45.60695570390418 | -23.37006569234464 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].net_per_hour_over_inc_std | -12.338018730430175 | -12.369756159268139 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].orders_per_fill | 1.2818247774365374 | 1.4121349007444646 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].own_edge_bp | 0.19366871542831335 | 0.17769037241798308 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].own_markout_1s_bp | -1.5728738008913108 | -1.5658171884482193 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].own_markout_30s_bp | -1.7909327203390948 | -1.7796848596319736 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].own_markout_5s_bp | -1.7572523686631087 | -1.7309809299512362 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].paced_spells | 4298.9 | 1164.8 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].paced_time_share | 0.0088720563459517 | 0.002465014151623335 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].quote_presence_ask | 0.5979688981432183 | 0.7784270625804248 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].quote_presence_bid | 0.622453180858349 | 0.8187162349500203 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].quote_presence_both | 0.31704518988751323 | 0.6266404291870611 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].turnover_per_hour | 38787.42725033309 | 20063.680153794332 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].tw_abs_inventory_avg | 6.391286316219372 | 5.69313523408167 |
| descriptive.scenarios[P3_M2/conservative/distant/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].fill_rate | 0.10348988097762027 | 0.13203404429564164 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].gate_active_share | 0.5140761299302854 | 0.23173997971877652 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].gross_bp_per_notional | -1.6939117548720266 | -1.5554078802549882 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].gross_per_hour | -6.707103806792469 | -3.222243212769102 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].inc_es | 6.725565233071881 | 3.443372604139891 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].inc_std | 2.170325520796755 | 1.0422505699084383 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].inc_worst | -12.71229598918109 | -6.589118818399422 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].max_abs_inventory | 10.613600000000078 | 10.436800000000034 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].max_drawdown | 252.60217582452023 | 132.2837997167374 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].net_bp_per_notional | -2.8018989268982124 | -2.6679336062226606 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].net_per_hour | -10.99957847308819 | -5.448600764616156 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].net_per_hour_over_inc_std | -4.688248080797792 | -4.975938322994852 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].orders_per_fill | 1.2818247774365374 | 1.4121349007444646 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].own_edge_bp | 0.19366871542831335 | 0.17769037241798308 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].own_markout_1s_bp | -1.5728738008913108 | -1.5658171884482193 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].own_markout_30s_bp | -1.7909327203390948 | -1.7796848596319736 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].own_markout_5s_bp | -1.7572523686631087 | -1.7309809299512362 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].paced_spells | 4298.9 | 1164.8 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].paced_time_share | 0.0088720563459517 | 0.002465014151623335 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].quote_presence_ask | 0.5979688981432183 | 0.7784270625804248 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].quote_presence_bid | 0.622453180858349 | 0.8187162349500203 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].quote_presence_both | 0.31704518988751323 | 0.6266404291870611 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].turnover_per_hour | 38787.42725033309 | 20063.680153794332 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].tw_abs_inventory_avg | 6.391286316219372 | 5.69313523408167 |
| descriptive.scenarios[P3_M2/conservative/distant/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].fill_rate | 0.08654132718377344 | 0.11043197140232892 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].gate_active_share | 0.5036680869393944 | 0.2204946164715539 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].gross_bp_per_notional | -1.7981396347427385 | -1.7360310716336538 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].gross_per_hour | -5.968587486800693 | -3.1172751908337846 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].inc_es | 5.587646008863091 | 3.002354021845341 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].inc_std | 2.057177106367163 | 1.026100286746197 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].inc_worst | -11.85767278808045 | -5.376549860479924 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].max_abs_inventory | 10.528900000000037 | 10.595200000000016 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].max_drawdown | 94.25784114159173 | 50.318546753216246 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].net_bp_per_notional | -1.008065745399088 | -0.9498242963747752 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].net_per_hour | -3.472869265930357 | -1.7912328010702043 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].net_per_hour_over_inc_std | -1.5483804891264015 | -1.60212005382652 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].orders_per_fill | 1.7415228305001598 | 1.8303806890572851 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].own_edge_bp | 0.15903042247994875 | 0.21518966191163988 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].own_markout_1s_bp | -1.7582795594169993 | -1.6493037239511164 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].own_markout_30s_bp | -2.0273470384834846 | -1.8031577041671647 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].own_markout_5s_bp | -1.9322848403705213 | -1.795735868370293 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].paced_spells | 4457.2 | 1151.4 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].paced_time_share | 0.008990057527196556 | 0.002417269384597889 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].quote_presence_ask | 0.6034122965998362 | 0.7737472388351079 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].quote_presence_bid | 0.6220483389123558 | 0.8124533227995332 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].quote_presence_both | 0.3203731100176248 | 0.6172810409907963 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].turnover_per_hour | 31534.56968837529 | 16795.760266142937 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].tw_abs_inventory_avg | 6.422311229266418 | 5.7824870485906334 |
| descriptive.scenarios[P3_M2/conservative/regional/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].fill_rate | 0.08654132718377344 | 0.11043197140232892 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].gate_active_share | 0.5036680869393944 | 0.2204946164715539 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].gross_bp_per_notional | -1.7981396347427385 | -1.7360310716336538 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].gross_per_hour | -5.968587486800693 | -3.1172751908337846 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].inc_es | 13.48047831416839 | 6.987661838799812 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].inc_std | 3.480715629753147 | 1.720234717438947 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].inc_worst | -23.578703583000326 | -12.343151421999698 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].max_abs_inventory | 10.528900000000037 | 10.595200000000016 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].max_drawdown | 848.6648979339718 | 478.76538637999465 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].net_bp_per_notional | -11.841296637596432 | -11.796001613986355 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].net_per_hour | -37.62075436734854 | -19.98963733318479 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].net_per_hour_over_inc_std | -10.274612339929906 | -11.020636138617164 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].orders_per_fill | 1.7415228305001598 | 1.8303806890572851 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].own_edge_bp | 0.15903042247994875 | 0.21518966191163988 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].own_markout_1s_bp | -1.7582795594169993 | -1.6493037239511164 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].own_markout_30s_bp | -2.0273470384834846 | -1.8031577041671647 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].own_markout_5s_bp | -1.9322848403705213 | -1.795735868370293 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].paced_spells | 4457.2 | 1151.4 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].paced_time_share | 0.008990057527196556 | 0.002417269384597889 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].quote_presence_ask | 0.6034122965998362 | 0.7737472388351079 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].quote_presence_bid | 0.6220483389123558 | 0.8124533227995332 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].quote_presence_both | 0.3203731100176248 | 0.6172810409907963 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].turnover_per_hour | 31534.56968837529 | 16795.760266142937 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].tw_abs_inventory_avg | 6.422311229266418 | 5.7824870485906334 |
| descriptive.scenarios[P3_M2/conservative/regional/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].fill_rate | 0.08654132718377344 | 0.11043197140232892 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].gate_active_share | 0.5036680869393944 | 0.2204946164715539 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].gross_bp_per_notional | -1.7981396347427385 | -1.7360310716336538 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].gross_per_hour | -5.968587486800693 | -3.1172751908337846 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].inc_es | 6.707597806195248 | 3.5777518880106514 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].inc_std | 2.189065589788153 | 1.0869755928324072 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].inc_worst | -13.579111464270728 | -6.441282767799945 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].max_abs_inventory | 10.528900000000037 | 10.595200000000016 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].max_drawdown | 219.33176503991407 | 121.05411643771554 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].net_bp_per_notional | -2.908065745399088 | -2.8498242963747753 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].net_per_hour | -9.464437506721662 | -4.982427251637363 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].net_per_hour_over_inc_std | -4.053694397075175 | -4.3312993010609695 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].orders_per_fill | 1.7415228305001598 | 1.8303806890572851 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].own_edge_bp | 0.15903042247994875 | 0.21518966191163988 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].own_markout_1s_bp | -1.7582795594169993 | -1.6493037239511164 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].own_markout_30s_bp | -2.0273470384834846 | -1.8031577041671647 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].own_markout_5s_bp | -1.9322848403705213 | -1.795735868370293 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].paced_spells | 4457.2 | 1151.4 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].paced_time_share | 0.008990057527196556 | 0.002417269384597889 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].quote_presence_ask | 0.6034122965998362 | 0.7737472388351079 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].quote_presence_bid | 0.6220483389123558 | 0.8124533227995332 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].quote_presence_both | 0.3203731100176248 | 0.6172810409907963 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].turnover_per_hour | 31534.56968837529 | 16795.760266142937 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].tw_abs_inventory_avg | 6.422311229266418 | 5.7824870485906334 |
| descriptive.scenarios[P3_M2/conservative/regional/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].fill_rate | 0.08728756757731773 | 0.09707269084775237 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].gate_active_share | 0.4905719408389545 | 0.21403541441424453 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].gross_bp_per_notional | -2.221720420018328 | -2.1764997594045092 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].gross_per_hour | -6.978842429483786 | -3.4711217728128654 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].inc_es | 5.681725848460202 | 2.933580915637328 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].inc_std | 2.0364987688983214 | 1.0355503274900377 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].inc_worst | -9.803184372638373 | -4.9195790232000025 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].max_abs_inventory | 10.090600000000062 | 9.993400000000024 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].max_drawdown | 116.11302629404713 | 60.70658011517757 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].net_bp_per_notional | -1.430088121504231 | -1.3914800159305851 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].net_per_hour | -4.537151586206611 | -2.269507153598039 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].net_per_hour_over_inc_std | -2.2672026671439913 | -2.1060502062977897 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].orders_per_fill | 2.009385905425705 | 2.3661851245510253 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].own_edge_bp | 0.34695554846221605 | 0.48479103377780886 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].own_markout_1s_bp | -2.2549472942119335 | -2.0609029395419616 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].own_markout_30s_bp | -2.578743239849636 | -2.195072299246571 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].own_markout_5s_bp | -2.4411480161952284 | -2.1951996208325726 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].paced_spells | 4517.5 | 1309.8 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].paced_time_share | 0.009109382730320598 | 0.002769890848236491 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].quote_presence_ask | 0.601443801597693 | 0.7736642620145442 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].quote_presence_bid | 0.6056895497206702 | 0.7964301490346356 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].quote_presence_both | 0.3084526088296552 | 0.6024913530569611 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].turnover_per_hour | 30846.774199625972 | 15242.328491334774 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].tw_abs_inventory_avg | 6.294343525442114 | 5.893586615621595 |
| descriptive.scenarios[P3_M2/conservative/tokyo/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].fill_rate | 0.08728756757731773 | 0.09707269084775237 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].gate_active_share | 0.4905719408389545 | 0.21403541441424453 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].gross_bp_per_notional | -2.221720420018328 | -2.1764997594045092 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].gross_per_hour | -6.978842429483786 | -3.4711217728128654 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].inc_es | 13.103613847652401 | 6.688344911733289 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].inc_std | 3.4414664357944282 | 1.7147470451213664 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].inc_worst | -21.233154418998474 | -11.237602363999699 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].max_abs_inventory | 10.090600000000062 | 9.993400000000024 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].max_drawdown | 856.3028202609752 | 450.0531472819969 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].net_bp_per_notional | -12.258101730826601 | -12.241631309517885 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].net_per_hour | -37.93888224951369 | -18.790718351503973 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].net_per_hour_over_inc_std | -10.450632632903837 | -10.369583143784492 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].orders_per_fill | 2.009385905425705 | 2.3661851245510253 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].own_edge_bp | 0.34695554846221605 | 0.48479103377780886 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].own_markout_1s_bp | -2.2549472942119335 | -2.0609029395419616 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].own_markout_30s_bp | -2.578743239849636 | -2.195072299246571 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].own_markout_5s_bp | -2.4411480161952284 | -2.1951996208325726 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].paced_spells | 4517.5 | 1309.8 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].paced_time_share | 0.009109382730320598 | 0.002769890848236491 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].quote_presence_ask | 0.601443801597693 | 0.7736642620145442 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].quote_presence_bid | 0.6056895497206702 | 0.7964301490346356 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].quote_presence_both | 0.3084526088296552 | 0.6024913530569611 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].turnover_per_hour | 30846.774199625972 | 15242.328491334774 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].tw_abs_inventory_avg | 6.294343525442114 | 5.893586615621595 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].fill_rate | 0.08728756757731773 | 0.09707269084775237 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].gate_active_share | 0.4905719408389545 | 0.21403541441424453 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].gross_bp_per_notional | -2.221720420018328 | -2.1764997594045092 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].gross_per_hour | -6.978842429483786 | -3.4711217728128654 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].inc_es | 6.703059486331843 | 3.5222060764399488 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].inc_std | 2.166379595912715 | 1.1073284160183539 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].inc_worst | -11.692498362618426 | -5.664376019659947 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].max_abs_inventory | 10.090600000000062 | 9.993400000000024 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].max_drawdown | 241.64994506900712 | 124.70523896291877 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].net_bp_per_notional | -3.330088121504231 | -3.291480015930585 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].net_per_hour | -10.398038684135546 | -5.165549566951646 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].net_per_hour_over_inc_std | -4.738442624552793 | -4.4465868419255985 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].orders_per_fill | 2.009385905425705 | 2.3661851245510253 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].own_edge_bp | 0.34695554846221605 | 0.48479103377780886 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].own_markout_1s_bp | -2.2549472942119335 | -2.0609029395419616 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].own_markout_30s_bp | -2.578743239849636 | -2.195072299246571 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].own_markout_5s_bp | -2.4411480161952284 | -2.1951996208325726 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].paced_spells | 4517.5 | 1309.8 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].paced_time_share | 0.009109382730320598 | 0.002769890848236491 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].quote_presence_ask | 0.601443801597693 | 0.7736642620145442 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].quote_presence_bid | 0.6056895497206702 | 0.7964301490346356 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].quote_presence_both | 0.3084526088296552 | 0.6024913530569611 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].turnover_per_hour | 30846.774199625972 | 15242.328491334774 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].tw_abs_inventory_avg | 6.294343525442114 | 5.893586615621595 |
| descriptive.scenarios[P3_M2/conservative/tokyo/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].fill_rate | 0.11775701650622668 | 0.16153351289452353 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].gate_active_share | 0.509798163829791 | 0.23094073167750784 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].gross_bp_per_notional | -1.528347311554396 | -1.4620379878839065 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].gross_per_hour | -6.8638666278294 | -3.6177020628339625 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].inc_es | 5.663062126275407 | 2.8927729520745653 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].inc_std | 2.079938525019947 | 1.002246229689301 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].inc_worst | -11.443282010799932 | -5.217158904319542 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].max_abs_inventory | 10.492800000000042 | 10.318000000000032 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].max_drawdown | 92.71272327390194 | 46.33870148603849 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].net_bp_per_notional | -0.7352646936367044 | -0.6712146395864584 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].net_per_hour | -3.4868220943467265 | -1.6987830472657985 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].net_per_hour_over_inc_std | -1.5264056270933226 | -1.6245632297355095 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].orders_per_fill | 1.3384748792520034 | 1.4864385933821105 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].own_edge_bp | 0.24367378392883174 | 0.29052057423592437 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].own_markout_1s_bp | -1.4171206696679095 | -1.325320536337916 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].own_markout_30s_bp | -1.6434188935578788 | -1.5465845783626777 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].own_markout_5s_bp | -1.5989174268985484 | -1.4972927324056446 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].paced_spells | 4302.7 | 1206.8 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].paced_time_share | 0.008846366945120646 | 0.0025752851819753585 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].quote_presence_ask | 0.5794501897517009 | 0.783870735853324 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].quote_presence_bid | 0.6288459636738414 | 0.8061678337412854 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].quote_presence_both | 0.30933349886772105 | 0.6185170615012006 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].turnover_per_hour | 42536.049960581564 | 24212.487691265535 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].tw_abs_inventory_avg | 6.507820352633084 | 5.62444378128323 |
| descriptive.scenarios[P3_M2/intermediate/distant/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].fill_rate | 0.11775701650622668 | 0.16153351289452353 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].gate_active_share | 0.509798163829791 | 0.23094073167750784 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].gross_bp_per_notional | -1.528347311554396 | -1.4620379878839065 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].gross_per_hour | -6.8638666278294 | -3.6177020628339625 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].inc_es | 13.84824844513199 | 7.954524895199893 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].inc_std | 3.4879855602629775 | 1.8623274389751945 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].inc_worst | -21.36299336999978 | -13.16496556399901 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].max_abs_inventory | 10.492800000000042 | 10.318000000000032 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].max_drawdown | 1111.3213633329165 | 668.3396551780012 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].net_bp_per_notional | -11.558422885825303 | -11.501936473547177 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].net_per_hour | -49.51226208129728 | -27.90879844859115 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].net_per_hour_over_inc_std | -13.463877657642456 | -14.231809373029048 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].orders_per_fill | 1.3384748792520034 | 1.4864385933821105 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].own_edge_bp | 0.24367378392883174 | 0.29052057423592437 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].own_markout_1s_bp | -1.4171206696679095 | -1.325320536337916 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].own_markout_30s_bp | -1.6434188935578788 | -1.5465845783626777 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].own_markout_5s_bp | -1.5989174268985484 | -1.4972927324056446 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].paced_spells | 4302.7 | 1206.8 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].paced_time_share | 0.008846366945120646 | 0.0025752851819753585 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].quote_presence_ask | 0.5794501897517009 | 0.783870735853324 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].quote_presence_bid | 0.6288459636738414 | 0.8061678337412854 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].quote_presence_both | 0.30933349886772105 | 0.6185170615012006 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].turnover_per_hour | 42536.049960581564 | 24212.487691265535 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].tw_abs_inventory_avg | 6.507820352633084 | 5.62444378128323 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].fill_rate | 0.11775701650622668 | 0.16153351289452353 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].gate_active_share | 0.509798163829791 | 0.23094073167750784 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].gross_bp_per_notional | -1.528347311554396 | -1.4620379878839065 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].gross_per_hour | -6.8638666278294 | -3.6177020628339625 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].inc_es | 6.852321634816531 | 3.6196933360491954 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].inc_std | 2.181573959174773 | 1.0648996404131372 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].inc_worst | -13.114923309120027 | -6.534437915819501 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].max_abs_inventory | 10.492800000000042 | 10.318000000000032 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].max_drawdown | 263.9003562249053 | 151.3883560552184 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].net_bp_per_notional | -2.635264693636705 | -2.5712146395864584 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].net_per_hour | -11.568671586857224 | -6.299155708606251 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].net_per_hour_over_inc_std | -4.958997734129745 | -5.635164797977243 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].orders_per_fill | 1.3384748792520034 | 1.4864385933821105 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].own_edge_bp | 0.24367378392883174 | 0.29052057423592437 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].own_markout_1s_bp | -1.4171206696679095 | -1.325320536337916 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].own_markout_30s_bp | -1.6434188935578788 | -1.5465845783626777 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].own_markout_5s_bp | -1.5989174268985484 | -1.4972927324056446 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].paced_spells | 4302.7 | 1206.8 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].paced_time_share | 0.008846366945120646 | 0.0025752851819753585 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].quote_presence_ask | 0.5794501897517009 | 0.783870735853324 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].quote_presence_bid | 0.6288459636738414 | 0.8061678337412854 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].quote_presence_both | 0.30933349886772105 | 0.6185170615012006 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].turnover_per_hour | 42536.049960581564 | 24212.487691265535 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].tw_abs_inventory_avg | 6.507820352633084 | 5.62444378128323 |
| descriptive.scenarios[P3_M2/intermediate/distant/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].fill_rate | 0.10131435638685937 | 0.13985396705946318 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].gate_active_share | 0.496898799404146 | 0.22174952603170225 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].gross_bp_per_notional | -1.7057728987484762 | -1.4864926590362693 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].gross_per_hour | -6.51037258383167 | -3.328294237230613 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].inc_es | 5.644001765649612 | 2.939970398719932 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].inc_std | 2.072620824551658 | 1.023358542639291 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].inc_worst | -11.737511660398987 | -5.300019066720317 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].liquidation_shortfall | 0.2246000000000005 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].max_abs_inventory | 10.490200000000048 | 10.691600000000024 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].max_drawdown | 94.43472486467397 | 46.323171497740596 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].net_bp_per_notional | -0.9139224157212731 | -0.6975921135916398 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].net_per_hour | -3.680713304886857 | -1.6372167241202409 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].net_per_hour_over_inc_std | -1.6263949565280076 | -1.496446388462608 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].orders_per_fill | 1.7729832791108744 | 1.8489635744280946 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].own_edge_bp | 0.20474857487241976 | 0.3016467444101144 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].own_markout_1s_bp | -1.5550349977096116 | -1.373335912469761 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].own_markout_30s_bp | -1.8127405389806661 | -1.5633350295141302 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].own_markout_5s_bp | -1.7154833605301074 | -1.5362596001170066 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].paced_spells | 4489.3 | 1192.8 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].paced_time_share | 0.00903935509442494 | 0.0024990998268517705 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].quote_presence_ask | 0.5813806080068107 | 0.7834901156313651 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].quote_presence_bid | 0.6277720030556855 | 0.8035992765419572 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].quote_presence_both | 0.3125048268833591 | 0.6172343600091551 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].turnover_per_hour | 35692.31475489134 | 21378.78230334543 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].tw_abs_inventory_avg | 6.528482140437307 | 5.84402596980161 |
| descriptive.scenarios[P3_M2/intermediate/regional/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].fill_rate | 0.10131435638685937 | 0.13985396705946318 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].gate_active_share | 0.496898799404146 | 0.22174952603170225 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].gross_bp_per_notional | -1.7057728987484762 | -1.4864926590362693 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].gross_per_hour | -6.51037258383167 | -3.328294237230613 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].inc_es | 14.032466228715297 | 7.710200198533192 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].inc_std | 3.5558069501284164 | 1.8256180765125234 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].inc_worst | -23.796861919998804 | -13.021969775999654 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].liquidation_shortfall | 0.2246000000000005 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].max_abs_inventory | 10.490200000000048 | 10.691600000000024 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].max_drawdown | 954.845421539975 | 593.6911923560031 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].net_bp_per_notional | -11.741205581238898 | -11.534751157103099 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].net_per_hour | -42.31453908414254 | -24.790663806477188 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].net_per_hour_over_inc_std | -11.500908615944429 | -12.974002570233855 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].orders_per_fill | 1.7729832791108744 | 1.8489635744280946 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].own_edge_bp | 0.20474857487241976 | 0.3016467444101144 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].own_markout_1s_bp | -1.5550349977096116 | -1.373335912469761 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].own_markout_30s_bp | -1.8127405389806661 | -1.5633350295141302 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].own_markout_5s_bp | -1.7154833605301074 | -1.5362596001170066 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].paced_spells | 4489.3 | 1192.8 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].paced_time_share | 0.00903935509442494 | 0.0024990998268517705 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].quote_presence_ask | 0.5813806080068107 | 0.7834901156313651 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].quote_presence_bid | 0.6277720030556855 | 0.8035992765419572 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].quote_presence_both | 0.3125048268833591 | 0.6172343600091551 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].turnover_per_hour | 35692.31475489134 | 21378.78230334543 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].tw_abs_inventory_avg | 6.528482140437307 | 5.84402596980161 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].fill_rate | 0.10131435638685937 | 0.13985396705946318 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].gate_active_share | 0.496898799404146 | 0.22174952603170225 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].gross_bp_per_notional | -1.7057728987484762 | -1.4864926590362693 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].gross_per_hour | -6.51037258383167 | -3.328294237230613 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].inc_es | 6.820663234244067 | 3.6464096770879175 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].inc_std | 2.205669457830102 | 1.0908079047256853 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].inc_worst | -13.472604900099308 | -6.47825412785985 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].liquidation_shortfall | 0.2246000000000005 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].max_abs_inventory | 10.490200000000048 | 10.691600000000024 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].max_drawdown | 240.6960578571055 | 137.28490394468082 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].net_bp_per_notional | -2.813922415721273 | -2.5975921135916398 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].net_per_hour | -10.462253108316212 | -5.699185361755873 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].net_per_hour_over_inc_std | -4.499109470210832 | -4.974041802214609 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].orders_per_fill | 1.7729832791108744 | 1.8489635744280946 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].own_edge_bp | 0.20474857487241976 | 0.3016467444101144 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].own_markout_1s_bp | -1.5550349977096116 | -1.373335912469761 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].own_markout_30s_bp | -1.8127405389806661 | -1.5633350295141302 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].own_markout_5s_bp | -1.7154833605301074 | -1.5362596001170066 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].paced_spells | 4489.3 | 1192.8 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].paced_time_share | 0.00903935509442494 | 0.0024990998268517705 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].quote_presence_ask | 0.5813806080068107 | 0.7834901156313651 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].quote_presence_bid | 0.6277720030556855 | 0.8035992765419572 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].quote_presence_both | 0.3125048268833591 | 0.6172343600091551 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].turnover_per_hour | 35692.31475489134 | 21378.78230334543 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].tw_abs_inventory_avg | 6.528482140437307 | 5.84402596980161 |
| descriptive.scenarios[P3_M2/intermediate/regional/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].fill_rate | 0.10066087568250252 | 0.12476534978596107 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].gate_active_share | 0.4899242212062734 | 0.2161064906451887 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].gross_bp_per_notional | -2.08229245411621 | -1.7668112062606034 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].gross_per_hour | -7.532491180944513 | -3.6059834547425225 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].inc_es | 5.815731413545057 | 2.8666862717120045 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].inc_std | 2.073533788684006 | 1.0182736110564476 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].inc_worst | -10.405826743600164 | -4.810661949279796 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].max_abs_inventory | 10.001700000000074 | 9.98980000000001 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].max_drawdown | 118.23355776965084 | 56.90098385047794 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].net_bp_per_notional | -1.2893147036758257 | -0.9791650747981293 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].net_per_hour | -4.784330623396761 | -2.0710146348444147 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].net_per_hour_over_inc_std | -2.302585074653094 | -1.9520362245956098 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].orders_per_fill | 1.9425373648791786 | 2.237917528987736 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].own_edge_bp | 0.357885399596391 | 0.5056377448875498 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].own_markout_1s_bp | -2.002386392632013 | -1.7291900174425492 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].own_markout_30s_bp | -2.3069135673010206 | -1.8631569951791138 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].own_markout_5s_bp | -2.1666409653542504 | -1.8597743913283729 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].paced_spells | 4511.3 | 1323.6 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].paced_time_share | 0.00907190730968309 | 0.002791933888694313 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].quote_presence_ask | 0.5877935722266131 | 0.7828012433462609 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].quote_presence_bid | 0.6130379699505187 | 0.7980340866831523 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].quote_presence_both | 0.3075494028064815 | 0.6126281855282694 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].turnover_per_hour | 34653.63028083927 | 19431.403166312062 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].tw_abs_inventory_avg | 6.3754656663699265 | 5.854928381833946 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].fill_rate | 0.10066087568250252 | 0.12476534978596107 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].gate_active_share | 0.4899242212062734 | 0.2161064906451887 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].gross_bp_per_notional | -2.08229245411621 | -1.7668112062606034 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].gross_per_hour | -7.532491180944513 | -3.6059834547425225 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].inc_es | 13.76634643772412 | 7.266769457333174 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].inc_std | 3.547790571455649 | 1.7793397696686857 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].inc_worst | -22.26023482699923 | -11.793441722000512 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].max_abs_inventory | 10.001700000000074 | 9.98980000000001 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].max_drawdown | 954.645875625973 | 553.7689591659973 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].net_bp_per_notional | -12.112823973940628 | -11.82052367816289 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].net_per_hour | -42.29103391795505 | -23.122358070649618 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].net_per_hour_over_inc_std | -11.442362987771972 | -12.43547032807797 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].orders_per_fill | 1.9425373648791786 | 2.237917528987736 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].own_edge_bp | 0.357885399596391 | 0.5056377448875498 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].own_markout_1s_bp | -2.002386392632013 | -1.7291900174425492 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].own_markout_30s_bp | -2.3069135673010206 | -1.8631569951791138 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].own_markout_5s_bp | -2.1666409653542504 | -1.8597743913283729 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].paced_spells | 4511.3 | 1323.6 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].paced_time_share | 0.00907190730968309 | 0.002791933888694313 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].quote_presence_ask | 0.5877935722266131 | 0.7828012433462609 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].quote_presence_bid | 0.6130379699505187 | 0.7980340866831523 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].quote_presence_both | 0.3075494028064815 | 0.6126281855282694 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].turnover_per_hour | 34653.63028083927 | 19431.403166312062 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].tw_abs_inventory_avg | 6.3754656663699265 | 5.854928381833946 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].fill_rate | 0.10066087568250252 | 0.12476534978596107 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].gate_active_share | 0.4899242212062734 | 0.2161064906451887 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].gross_bp_per_notional | -2.08229245411621 | -1.7668112062606034 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].gross_per_hour | -7.532491180944513 | -3.6059834547425225 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].inc_es | 6.891673101521337 | 3.5458106313653133 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].inc_std | 2.209647581227719 | 1.0933512230199693 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].inc_worst | -12.00179650663959 | -5.639122897580346 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].max_abs_inventory | 10.001700000000074 | 9.98980000000001 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].max_drawdown | 261.9041789836513 | 138.3657349208765 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].net_bp_per_notional | -3.1893147036758256 | -2.8791650747981294 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].net_per_hour | -11.368520376756223 | -5.762981236443707 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].net_per_hour_over_inc_std | -5.090792235813966 | -5.05238566623637 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].orders_per_fill | 1.9425373648791786 | 2.237917528987736 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].own_edge_bp | 0.357885399596391 | 0.5056377448875498 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].own_markout_1s_bp | -2.002386392632013 | -1.7291900174425492 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].own_markout_30s_bp | -2.3069135673010206 | -1.8631569951791138 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].own_markout_5s_bp | -2.1666409653542504 | -1.8597743913283729 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].paced_spells | 4511.3 | 1323.6 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].paced_time_share | 0.00907190730968309 | 0.002791933888694313 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].quote_presence_ask | 0.5877935722266131 | 0.7828012433462609 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].quote_presence_bid | 0.6130379699505187 | 0.7980340866831523 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].quote_presence_both | 0.3075494028064815 | 0.6126281855282694 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].turnover_per_hour | 34653.63028083927 | 19431.403166312062 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].tw_abs_inventory_avg | 6.3754656663699265 | 5.854928381833946 |
| descriptive.scenarios[P3_M2/intermediate/tokyo/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].fill_rate | 0.19640170003259871 | 0.30359829700506225 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].gate_active_share | 0.49430238934502047 | 0.22746741428241166 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].gross_bp_per_notional | -1.1550206933867462 | -0.9190548636736731 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].gross_per_hour | -8.66775368391464 | -4.552042508971004 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].inc_es | 5.686522042062361 | 2.739682088650455 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].inc_std | 2.1216464275009295 | 1.0122765902173274 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].inc_worst | -11.25517930360061 | -4.975769805760163 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].liquidation_shortfall | 0.532199999999999 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].max_abs_inventory | 10.520499999999945 | 10.120199999999977 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].max_drawdown | 90.31853780080888 | 31.820419306416774 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].net_bp_per_notional | -0.35959122729356247 | -0.12276496784074373 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].net_per_hour | -3.258359084772354 | -0.6257891660211683 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].net_per_hour_over_inc_std | -1.3563389834351356 | -0.6456438969222394 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].orders_per_fill | 1.2164541870274663 | 1.2275732442618743 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].own_edge_bp | 0.4267415051858598 | 0.5821974703344729 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].own_markout_1s_bp | -0.9583304866140374 | -0.8034754626624345 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].own_markout_30s_bp | -1.1777403009314156 | -1.0134893892917964 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].own_markout_5s_bp | -1.1204898009211983 | -0.97500233089884 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].paced_spells | 4927.7 | 1602.2 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].paced_time_share | 0.009918010113305585 | 0.003348706486868331 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].quote_presence_ask | 0.559477823589924 | 0.7840490448986384 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].quote_presence_bid | 0.6285130800271017 | 0.7904161881841917 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].quote_presence_both | 0.29919135412821296 | 0.6016739516718838 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].turnover_per_hour | 67963.13753855546 | 49292.059073819975 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].tw_abs_inventory_avg | 6.6691744156805 | 5.781429716468913 |
| descriptive.scenarios[P3_M2/optimistic/distant/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].fill_rate | 0.19640170003259871 | 0.30359829700506225 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].gate_active_share | 0.49430238934502047 | 0.22746741428241166 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].gross_bp_per_notional | -1.1550206933867462 | -0.9190548636736731 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].gross_per_hour | -8.66775368391464 | -4.552042508971004 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].inc_es | 17.77156480420111 | 12.890241429333262 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].inc_std | 4.30001537167689 | 2.8542027572244058 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].inc_worst | -25.27319199099972 | -19.100610738000988 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].liquidation_shortfall | 0.532199999999999 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].max_abs_inventory | 10.520499999999945 | 10.120199999999977 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].max_drawdown | 1732.3913670529448 | 1290.7056105120141 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].net_bp_per_notional | -11.17489257993812 | -10.935185751356588 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].net_per_hour | -76.7511364570012 | -53.91849889998995 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].net_per_hour_over_inc_std | -17.215594657638142 | -18.022848247830336 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].orders_per_fill | 1.2164541870274663 | 1.2275732442618743 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].own_edge_bp | 0.4267415051858598 | 0.5821974703344729 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].own_markout_1s_bp | -0.9583304866140374 | -0.8034754626624345 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].own_markout_30s_bp | -1.1777403009314156 | -1.0134893892917964 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].own_markout_5s_bp | -1.1204898009211983 | -0.97500233089884 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].paced_spells | 4927.7 | 1602.2 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].paced_time_share | 0.009918010113305585 | 0.003348706486868331 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].quote_presence_ask | 0.559477823589924 | 0.7840490448986384 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].quote_presence_bid | 0.6285130800271017 | 0.7904161881841917 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].quote_presence_both | 0.29919135412821296 | 0.6016739516718838 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].turnover_per_hour | 67963.13753855546 | 49292.059073819975 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].tw_abs_inventory_avg | 6.6691744156805 | 5.781429716468913 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].fill_rate | 0.19640170003259871 | 0.30359829700506225 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].gate_active_share | 0.49430238934502047 | 0.22746741428241166 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].gross_bp_per_notional | -1.1550206933867462 | -0.9190548636736731 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].gross_per_hour | -8.66775368391464 | -4.552042508971004 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].inc_es | 7.443566434581115 | 4.1950946379745 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].inc_std | 2.266468151145856 | 1.1501229342246075 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].inc_worst | -13.528482651591068 | -7.0699209197002 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].liquidation_shortfall | 0.532199999999999 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].max_abs_inventory | 10.520499999999945 | 10.120199999999977 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].max_drawdown | 368.9765545002344 | 239.1927244342782 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].net_bp_per_notional | -2.2595912272935625 | -2.022764967840744 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].net_per_hour | -16.17135521709789 | -9.991280390046963 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].net_per_hour_over_inc_std | -6.919585599531773 | -8.311503623637142 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].orders_per_fill | 1.2164541870274663 | 1.2275732442618743 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].own_edge_bp | 0.4267415051858598 | 0.5821974703344729 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].own_markout_1s_bp | -0.9583304866140374 | -0.8034754626624345 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].own_markout_30s_bp | -1.1777403009314156 | -1.0134893892917964 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].own_markout_5s_bp | -1.1204898009211983 | -0.97500233089884 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].paced_spells | 4927.7 | 1602.2 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].paced_time_share | 0.009918010113305585 | 0.003348706486868331 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].quote_presence_ask | 0.559477823589924 | 0.7840490448986384 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].quote_presence_bid | 0.6285130800271017 | 0.7904161881841917 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].quote_presence_both | 0.29919135412821296 | 0.6016739516718838 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].turnover_per_hour | 67963.13753855546 | 49292.059073819975 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].tw_abs_inventory_avg | 6.6691744156805 | 5.781429716468913 |
| descriptive.scenarios[P3_M2/optimistic/distant/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].fill_rate | 0.18040766090409374 | 0.289545678779722 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].gate_active_share | 0.4793038545173591 | 0.21665881923104008 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].gross_bp_per_notional | -1.1894484536073542 | -0.9726916045525247 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].gross_per_hour | -8.362892988524454 | -4.846220814458851 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].inc_es | 5.750292455788935 | 2.999203565738602 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].inc_std | 2.111375104987444 | 1.0603727911508833 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].inc_worst | -10.059072711119825 | -5.273682338720464 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].liquidation_shortfall | 0.5300999999999993 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].max_abs_inventory | 10.489899999999967 | 10.204000000000013 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].max_drawdown | 96.3032604332874 | 37.15131606537691 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].net_bp_per_notional | -0.39483714934626246 | -0.17750476002049703 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].net_per_hour | -3.494188000209107 | -0.9617559911555841 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].net_per_hour_over_inc_std | -1.4364323813758957 | -0.8653585974273386 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].orders_per_fill | 1.4696142005073232 | 1.3302223036329228 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].own_edge_bp | 0.4158120164591598 | 0.5784106328286454 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].own_markout_1s_bp | -1.0275723962884609 | -0.8416324299997671 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].own_markout_30s_bp | -1.2337760863464362 | -1.0524466522589204 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].own_markout_5s_bp | -1.158776052441526 | -1.0043538251352546 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].paced_spells | 5467.2 | 1856.8 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].paced_time_share | 0.010473167756773625 | 0.003743637428646092 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].quote_presence_ask | 0.5568869268016181 | 0.7846248394726544 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].quote_presence_bid | 0.6320714456347568 | 0.7975044477356958 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].quote_presence_both | 0.30647052982631035 | 0.6111077041711118 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].turnover_per_hour | 61225.337169273014 | 48818.56110332722 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].tw_abs_inventory_avg | 6.7711979903637145 | 5.9241392311655385 |
| descriptive.scenarios[P3_M2/optimistic/regional/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].fill_rate | 0.18040766090409374 | 0.289545678779722 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].gate_active_share | 0.4793038545173591 | 0.21665881923104008 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].gross_bp_per_notional | -1.1894484536073542 | -0.9726916045525247 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].gross_per_hour | -8.362892988524454 | -4.846220814458851 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].inc_es | 18.6495829033476 | 13.82508808613336 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].inc_std | 4.491894946118122 | 3.049500940456577 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].inc_worst | -28.311466285996726 | -21.360510713997606 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].liquidation_shortfall | 0.5300999999999993 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].max_abs_inventory | 10.489899999999967 | 10.204000000000013 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].max_drawdown | 1580.815689062944 | 1286.947092456015 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].net_bp_per_notional | -11.212877565515651 | -10.993618367456751 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].net_per_hour | -69.71571705008657 | -53.75617350458133 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].net_per_hour_over_inc_std | -15.124695234510693 | -16.86533798782246 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].orders_per_fill | 1.4696142005073232 | 1.3302223036329228 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].own_edge_bp | 0.4158120164591598 | 0.5784106328286454 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].own_markout_1s_bp | -1.0275723962884609 | -0.8416324299997671 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].own_markout_30s_bp | -1.2337760863464362 | -1.0524466522589204 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].own_markout_5s_bp | -1.158776052441526 | -1.0043538251352546 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].paced_spells | 5467.2 | 1856.8 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].paced_time_share | 0.010473167756773625 | 0.003743637428646092 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].quote_presence_ask | 0.5568869268016181 | 0.7846248394726544 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].quote_presence_bid | 0.6320714456347568 | 0.7975044477356958 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].quote_presence_both | 0.30647052982631035 | 0.6111077041711118 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].turnover_per_hour | 61225.337169273014 | 48818.56110332722 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].tw_abs_inventory_avg | 6.7711979903637145 | 5.9241392311655385 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].fill_rate | 0.18040766090409374 | 0.289545678779722 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].gate_active_share | 0.4793038545173591 | 0.21665881923104008 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].gross_bp_per_notional | -1.1894484536073542 | -0.9726916045525247 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].gross_per_hour | -8.362892988524454 | -4.846220814458851 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].inc_es | 7.618479249023061 | 4.64341085026933 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].inc_std | 2.3257053368299605 | 1.2487980750360637 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].inc_worst | -12.734522227959747 | -7.958241120059815 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].liquidation_shortfall | 0.5300999999999993 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].max_abs_inventory | 10.489899999999967 | 10.204000000000013 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].max_drawdown | 347.6842973134147 | 245.17193446763912 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].net_bp_per_notional | -2.2948371493462627 | -2.077504760020497 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].net_per_hour | -15.12700206237098 | -10.237282600787758 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].net_per_hour_over_inc_std | -6.416899066447412 | -7.8121274758665695 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].orders_per_fill | 1.4696142005073232 | 1.3302223036329228 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].own_edge_bp | 0.4158120164591598 | 0.5784106328286454 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].own_markout_1s_bp | -1.0275723962884609 | -0.8416324299997671 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].own_markout_30s_bp | -1.2337760863464362 | -1.0524466522589204 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].own_markout_5s_bp | -1.158776052441526 | -1.0043538251352546 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].paced_spells | 5467.2 | 1856.8 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].paced_time_share | 0.010473167756773625 | 0.003743637428646092 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].quote_presence_ask | 0.5568869268016181 | 0.7846248394726544 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].quote_presence_bid | 0.6320714456347568 | 0.7975044477356958 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].quote_presence_both | 0.30647052982631035 | 0.6111077041711118 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].turnover_per_hour | 61225.337169273014 | 48818.56110332722 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].tw_abs_inventory_avg | 6.7711979903637145 | 5.9241392311655385 |
| descriptive.scenarios[P3_M2/optimistic/regional/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].fill_rate | 0.20052405549414137 | 0.3105881445906814 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].gate_active_share | 0.4813656887693189 | 0.212254136347474 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].gross_bp_per_notional | -1.4960418276536527 | -1.2031380009481154 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].gross_per_hour | -11.104579114395978 | -6.762114678552733 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].inc_es | 6.0011719844238725 | 3.139043557269276 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].inc_std | 2.122716875677676 | 1.0756698129214848 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].inc_worst | -11.26574180240181 | -5.610948355679769 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].liquidation_shortfall | 0.08649999999999787 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].max_abs_inventory | 9.998000000000044 | 9.996000000000048 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].max_drawdown | 138.4107238483966 | 64.72827106503212 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].net_bp_per_notional | -0.7004548651632215 | -0.40698712667366166 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].net_per_hour | -5.604681693204137 | -2.415284070585859 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].net_per_hour_over_inc_std | -2.5481118931398963 | -2.0926818077359686 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].orders_per_fill | 1.4677503352033692 | 1.283653187367368 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].own_edge_bp | 0.41344001652633755 | 0.5775314014928628 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].own_markout_1s_bp | -1.3472070563711818 | -1.068453010047674 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].own_markout_30s_bp | -1.5684097113449615 | -1.2503912517041826 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].own_markout_5s_bp | -1.479647163766706 | -1.2124738258865437 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].paced_spells | 5377.8 | 1605.6 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].paced_time_share | 0.010385977626262841 | 0.003304200957487171 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].quote_presence_ask | 0.5724495901441145 | 0.7847535168322445 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].quote_presence_bid | 0.627361722956782 | 0.8001304227036752 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].quote_presence_both | 0.31158973274428037 | 0.6146474562673838 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].turnover_per_hour | 69095.23784389014 | 54569.8417294323 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].tw_abs_inventory_avg | 6.438898437295824 | 5.754938115413541 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].fill_rate | 0.20052405549414137 | 0.3105881445906814 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].gate_active_share | 0.4813656887693189 | 0.212254136347474 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].gross_bp_per_notional | -1.4960418276536527 | -1.2031380009481154 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].gross_per_hour | -11.104579114395978 | -6.762114678552733 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].inc_es | 20.25963249372339 | 15.32934146559983 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].inc_std | 4.88694935757902 | 3.420000045852466 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].inc_worst | -30.865582718001225 | -22.806062782001163 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].liquidation_shortfall | 0.08649999999999787 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].max_abs_inventory | 9.998000000000044 | 9.996000000000048 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].max_drawdown | 1821.9092759619787 | 1470.4592114640134 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].net_bp_per_notional | -11.515228947260475 | -11.219873330189621 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].net_per_hour | -80.32034568141383 | -61.41350740967073 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].net_per_hour_over_inc_std | -15.747589872959619 | -17.20414376690752 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].orders_per_fill | 1.4677503352033692 | 1.283653187367368 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].own_edge_bp | 0.41344001652633755 | 0.5775314014928628 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].own_markout_1s_bp | -1.3472070563711818 | -1.068453010047674 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].own_markout_30s_bp | -1.5684097113449615 | -1.2503912517041826 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].own_markout_5s_bp | -1.479647163766706 | -1.2124738258865437 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].paced_spells | 5377.8 | 1605.6 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].paced_time_share | 0.010385977626262841 | 0.003304200957487171 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].quote_presence_ask | 0.5724495901441145 | 0.7847535168322445 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].quote_presence_bid | 0.627361722956782 | 0.8001304227036752 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].quote_presence_both | 0.31158973274428037 | 0.6146474562673838 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].turnover_per_hour | 69095.23784389014 | 54569.8417294323 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].tw_abs_inventory_avg | 6.438898437295824 | 5.754938115413541 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].fill_rate | 0.20052405549414137 | 0.3105881445906814 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].gate_active_share | 0.4813656887693189 | 0.212254136347474 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].gross_bp_per_notional | -1.4960418276536527 | -1.2031380009481154 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].gross_per_hour | -11.104579114395978 | -6.762114678552733 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].inc_es | 8.067299102835015 | 4.952581802339971 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].inc_std | 2.3932279747283056 | 1.3289357377331281 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].inc_worst | -14.073714746620604 | -8.523633980759723 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].liquidation_shortfall | 0.08649999999999787 | 0.0 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].max_abs_inventory | 9.998000000000044 | 9.996000000000048 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].max_drawdown | 429.55258518773644 | 306.2469031787388 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].net_bp_per_notional | -2.6004548651632216 | -2.306987126673662 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].net_per_hour | -18.732776883543263 | -12.783553999177997 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].net_per_hour_over_inc_std | -7.6813365951183155 | -9.142553377748081 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].orders_per_fill | 1.4677503352033692 | 1.283653187367368 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].own_edge_bp | 0.41344001652633755 | 0.5775314014928628 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].own_markout_1s_bp | -1.3472070563711818 | -1.068453010047674 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].own_markout_30s_bp | -1.5684097113449615 | -1.2503912517041826 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].own_markout_5s_bp | -1.479647163766706 | -1.2124738258865437 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].paced_spells | 5377.8 | 1605.6 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].paced_time_share | 0.010385977626262841 | 0.003304200957487171 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].quote_presence_ask | 0.5724495901441145 | 0.7847535168322445 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].quote_presence_bid | 0.627361722956782 | 0.8001304227036752 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].quote_presence_both | 0.31158973274428037 | 0.6146474562673838 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].turnover_per_hour | 69095.23784389014 | 54569.8417294323 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].tw_abs_inventory_avg | 6.438898437295824 | 5.754938115413541 |
| descriptive.scenarios[P3_M2/optimistic/tokyo/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].fill_rate | 0.2784790586619371 | 0.22191604099486578 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].gate_active_share | 0.5750573766818907 | 0.2585224483087585 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].gross_bp_per_notional | -1.6897149970429293 | -1.6233469876174298 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].gross_per_hour | -17.239771268092795 | -5.876602788899228 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].inc_es | 5.951673430547897 | 3.0105581671678485 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].inc_std | 1.8976789600376975 | 0.9694587291366092 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].inc_worst | -11.750996541119035 | -4.941135635839387 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].liquidation_shortfall | 0.47670000000000384 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].max_abs_inventory | 10.584400000000253 | 10.844399999999995 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].max_drawdown | 207.68250623941327 | 75.569306265448 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].net_bp_per_notional | -0.8926140437692827 | -0.8304164939124117 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].net_per_hour | -9.209520310008884 | -2.997789199761924 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].net_per_hour_over_inc_std | -4.2014637953449325 | -2.86329802783165 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].orders_per_fill | 0.6057909058064757 | 0.9211653583149427 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].own_edge_bp | 0.18909382232665992 | 0.21435641049631543 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].own_markout_1s_bp | -1.3393867378356772 | -1.4043334139932644 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].own_markout_30s_bp | -1.6629884926554765 | -1.6765653853307814 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].own_markout_5s_bp | -1.5491104007936323 | -1.6005974206770748 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].paced_spells | 4912.5 | 1482.2 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].paced_time_share | 0.010602059198559246 | 0.0032366124789777436 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].quote_presence_ask | 0.5967957060299179 | 0.7794093499908744 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].quote_presence_bid | 0.6137766730464073 | 0.8026130636625199 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].quote_presence_both | 0.3417421860014362 | 0.6301064046020803 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].turnover_per_hour | 100730.67736280612 | 36227.49577472597 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].tw_abs_inventory_avg | 5.655920760634954 | 5.582403756044057 |
| descriptive.scenarios[P3_negM2/conservative/distant/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].fill_rate | 0.2784790586619371 | 0.22191604099486578 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].gate_active_share | 0.5750573766818907 | 0.2585224483087585 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].gross_bp_per_notional | -1.6897149970429293 | -1.6233469876174298 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].gross_per_hour | -17.239771268092795 | -5.876602788899228 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].inc_es | 21.11490190078924 | 10.779159774799862 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].inc_std | 4.48405077214039 | 2.481803874584318 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].inc_worst | -29.744344596998957 | -15.349321855999275 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].liquidation_shortfall | 0.47670000000000384 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].max_abs_inventory | 10.584400000000253 | 10.844399999999995 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].max_drawdown | 2588.8667301417677 | 1010.4173731600247 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].net_bp_per_notional | -11.702319548027074 | -11.654083971508658 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].net_per_hour | -118.09307137411881 | -42.18838583684596 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].net_per_hour_over_inc_std | -23.233373921681512 | -15.882192202648213 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].orders_per_fill | 0.6057909058064757 | 0.9211653583149427 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].own_edge_bp | 0.18909382232665992 | 0.21435641049631543 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].own_markout_1s_bp | -1.3393867378356772 | -1.4043334139932644 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].own_markout_30s_bp | -1.6629884926554765 | -1.6765653853307814 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].own_markout_5s_bp | -1.5491104007936323 | -1.6005974206770748 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].paced_spells | 4912.5 | 1482.2 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].paced_time_share | 0.010602059198559246 | 0.0032366124789777436 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].quote_presence_ask | 0.5967957060299179 | 0.7794093499908744 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].quote_presence_bid | 0.6137766730464073 | 0.8026130636625199 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].quote_presence_both | 0.3417421860014362 | 0.6301064046020803 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].turnover_per_hour | 100730.67736280612 | 36227.49577472597 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].tw_abs_inventory_avg | 5.655920760634954 | 5.582403756044057 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].fill_rate | 0.2784790586619371 | 0.22191604099486578 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].gate_active_share | 0.5750573766818907 | 0.2585224483087585 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].gross_bp_per_notional | -1.6897149970429293 | -1.6233469876174298 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].gross_per_hour | -17.239771268092795 | -5.876602788899228 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].inc_es | 8.165235861879953 | 4.066049323601208 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].inc_std | 2.0723680476829798 | 1.1010517436597622 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].inc_worst | -14.640912011439536 | -6.442606081119564 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].liquidation_shortfall | 0.47670000000000384 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].max_abs_inventory | 10.584400000000253 | 10.844399999999995 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].max_drawdown | 623.7476783723436 | 237.2227021111327 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].net_bp_per_notional | -2.792614043769283 | -2.730416493912412 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].net_per_hour | -28.348349008942044 | -9.881013396959858 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].net_per_hour_over_inc_std | -11.971688758850217 | -8.320329857177699 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].orders_per_fill | 0.6057909058064757 | 0.9211653583149427 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].own_edge_bp | 0.18909382232665992 | 0.21435641049631543 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].own_markout_1s_bp | -1.3393867378356772 | -1.4043334139932644 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].own_markout_30s_bp | -1.6629884926554765 | -1.6765653853307814 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].own_markout_5s_bp | -1.5491104007936323 | -1.6005974206770748 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].paced_spells | 4912.5 | 1482.2 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].paced_time_share | 0.010602059198559246 | 0.0032366124789777436 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].quote_presence_ask | 0.5967957060299179 | 0.7794093499908744 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].quote_presence_bid | 0.6137766730464073 | 0.8026130636625199 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].quote_presence_both | 0.3417421860014362 | 0.6301064046020803 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].turnover_per_hour | 100730.67736280612 | 36227.49577472597 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].tw_abs_inventory_avg | 5.655920760634954 | 5.582403756044057 |
| descriptive.scenarios[P3_negM2/conservative/distant/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].fill_rate | 0.2859252429330068 | 0.21423882123900428 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].gate_active_share | 0.5803740080887995 | 0.25846958195712705 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].gross_bp_per_notional | -1.69520700873437 | -1.689668455821493 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].gross_per_hour | -23.33323320454364 | -6.614706898130794 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].inc_es | 6.589320881808628 | 3.1240724955732784 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].inc_std | 2.0020214543046153 | 1.0031971419862387 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].inc_worst | -13.504553422718487 | -4.758435614399855 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].liquidation_shortfall | 0.5265000000000054 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].max_abs_inventory | 10.854700000000618 | 10.69999999999995 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].max_drawdown | 277.36372392157125 | 86.23201948153364 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].net_bp_per_notional | -0.8975719117380645 | -0.8967312219027214 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].net_per_hour | -12.43642984028645 | -3.46936729890628 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].net_per_hour_over_inc_std | -5.256688227065182 | -3.2239949507414685 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].orders_per_fill | 0.5239426950822141 | 0.8957742486152199 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].own_edge_bp | 0.15839459994599475 | 0.24082110676269464 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].own_markout_1s_bp | -1.4135832619736302 | -1.4548403069160505 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].own_markout_30s_bp | -1.7196905736687373 | -1.7108572867209375 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].own_markout_5s_bp | -1.6163372615949734 | -1.64974733659411 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].paced_spells | 5295.7 | 1426.0 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].paced_time_share | 0.011567753719716104 | 0.003160434827547229 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].quote_presence_ask | 0.6125017194681301 | 0.7767956645316103 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].quote_presence_bid | 0.628351240725481 | 0.8027244013083792 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].quote_presence_both | 0.34469814679505295 | 0.618334300357256 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].turnover_per_hour | 136624.51874418845 | 39565.7139881063 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].tw_abs_inventory_avg | 5.6712847439024845 | 5.698969749232598 |
| descriptive.scenarios[P3_negM2/conservative/regional/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].fill_rate | 0.2859252429330068 | 0.21423882123900428 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].gate_active_share | 0.5803740080887995 | 0.25846958195712705 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].gross_bp_per_notional | -1.69520700873437 | -1.689668455821493 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].gross_per_hour | -23.33323320454364 | -6.614706898130794 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].inc_es | 30.799108813422798 | 12.5605782876004 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].inc_std | 6.650433166968158 | 2.919148754441406 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].inc_worst | -43.41756312899421 | -18.905639233997867 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].liquidation_shortfall | 0.5265000000000054 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].max_abs_inventory | 10.854700000000618 | 10.69999999999995 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].max_drawdown | 3487.3054929717173 | 1108.2063417480435 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].net_bp_per_notional | -11.705489195706956 | -11.72037613443553 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].net_per_hour | -160.10191775428817 | -46.2670187985153 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].net_per_hour_over_inc_std | -21.15162580148941 | -14.791063189745163 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].orders_per_fill | 0.5239426950822141 | 0.8957742486152199 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].own_edge_bp | 0.15839459994599475 | 0.24082110676269464 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].own_markout_1s_bp | -1.4135832619736302 | -1.4548403069160505 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].own_markout_30s_bp | -1.7196905736687373 | -1.7108572867209375 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].own_markout_5s_bp | -1.6163372615949734 | -1.64974733659411 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].paced_spells | 5295.7 | 1426.0 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].paced_time_share | 0.011567753719716104 | 0.003160434827547229 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].quote_presence_ask | 0.6125017194681301 | 0.7767956645316103 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].quote_presence_bid | 0.628351240725481 | 0.8027244013083792 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].quote_presence_both | 0.34469814679505295 | 0.618334300357256 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].turnover_per_hour | 136624.51874418845 | 39565.7139881063 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].tw_abs_inventory_avg | 5.6712847439024845 | 5.698969749232598 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].fill_rate | 0.2859252429330068 | 0.21423882123900428 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].gate_active_share | 0.5803740080887995 | 0.25846958195712705 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].gross_bp_per_notional | -1.69520700873437 | -1.689668455821493 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].gross_per_hour | -23.33323320454364 | -6.614706898130794 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].inc_es | 10.169254279028758 | 4.478439521972098 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].inc_std | 2.4621609818005092 | 1.1942288418138163 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].inc_worst | -18.247561606257808 | -6.656896810118965 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].liquidation_shortfall | 0.5265000000000054 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].max_abs_inventory | 10.854700000000618 | 10.69999999999995 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].max_drawdown | 839.2504114574485 | 263.63150956357856 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].net_bp_per_notional | -2.797571911738065 | -2.7967312219027214 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].net_per_hour | -38.39508840168226 | -10.986852956646477 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].net_per_hour_over_inc_std | -13.379736104278257 | -8.539542277766627 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].orders_per_fill | 0.5239426950822141 | 0.8957742486152199 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].own_edge_bp | 0.15839459994599475 | 0.24082110676269464 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].own_markout_1s_bp | -1.4135832619736302 | -1.4548403069160505 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].own_markout_30s_bp | -1.7196905736687373 | -1.7108572867209375 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].own_markout_5s_bp | -1.6163372615949734 | -1.64974733659411 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].paced_spells | 5295.7 | 1426.0 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].paced_time_share | 0.011567753719716104 | 0.003160434827547229 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].quote_presence_ask | 0.6125017194681301 | 0.7767956645316103 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].quote_presence_bid | 0.628351240725481 | 0.8027244013083792 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].quote_presence_both | 0.34469814679505295 | 0.618334300357256 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].turnover_per_hour | 136624.51874418845 | 39565.7139881063 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].tw_abs_inventory_avg | 5.6712847439024845 | 5.698969749232598 |
| descriptive.scenarios[P3_negM2/conservative/regional/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].fill_rate | 0.2922732735255555 | 0.19899277128228748 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].gate_active_share | 0.5747566764372011 | 0.25478951909896486 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].gross_bp_per_notional | -1.8761399299780515 | -1.908683799302582 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].gross_per_hour | -28.24158102676596 | -7.4354443449602625 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].inc_es | 6.904250803181215 | 3.257047684672004 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].inc_std | 2.047425243380185 | 1.0344737425824122 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].inc_worst | -12.61108530287714 | -5.17473623679985 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].liquidation_shortfall | 0.48130000000000717 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].max_abs_inventory | 10.459500000000098 | 10.06020000000008 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].max_drawdown | 352.1830534327338 | 104.91764618705352 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].net_bp_per_notional | -1.0779676486307248 | -1.1148919756077598 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].net_per_hour | -16.00160542423485 | -4.274782474145832 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].net_per_hour_over_inc_std | -6.756498323378726 | -3.8719791365354856 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].orders_per_fill | 0.5113426638028106 | 0.961967467174374 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].own_edge_bp | 0.342297558327605 | 0.5098615739335679 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].own_markout_1s_bp | -1.6260853772700503 | -1.6481554750929877 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].own_markout_30s_bp | -1.910112942118399 | -1.8757364576287165 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].own_markout_5s_bp | -1.8209926138709793 | -1.826531513714097 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].paced_spells | 5489.8 | 1592.6 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].paced_time_share | 0.0121712162448623 | 0.003578428264200746 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].quote_presence_ask | 0.6100162107082928 | 0.7827945102855332 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].quote_presence_bid | 0.60713050465246 | 0.7874512321627759 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].quote_presence_both | 0.32500373735836574 | 0.6091211681049271 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].turnover_per_hour | 153403.67574002955 | 39722.79733979609 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].tw_abs_inventory_avg | 5.944278048143927 | 5.786794472680201 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].fill_rate | 0.2922732735255555 | 0.19899277128228748 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].gate_active_share | 0.5747566764372011 | 0.25478951909896486 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].gross_bp_per_notional | -1.8761399299780515 | -1.908683799302582 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].gross_per_hour | -28.24158102676596 | -7.4354443449602625 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].inc_es | 33.84706736739801 | 12.406631580667014 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].inc_std | 7.31107704652235 | 2.92571148936218 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].inc_worst | -44.45761655899024 | -18.870812441999384 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].liquidation_shortfall | 0.48130000000000717 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].max_abs_inventory | 10.459500000000098 | 10.06020000000008 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].max_drawdown | 3948.4331485306707 | 1131.4880094480457 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].net_bp_per_notional | -11.884086532815761 | -11.93567587019466 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].net_per_hour | -181.78577179580094 | -47.23285871244877 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].net_per_hour_over_inc_std | -21.851996354100557 | -14.931697093747847 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].orders_per_fill | 0.5113426638028106 | 0.961967467174374 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].own_edge_bp | 0.342297558327605 | 0.5098615739335679 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].own_markout_1s_bp | -1.6260853772700503 | -1.6481554750929877 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].own_markout_30s_bp | -1.910112942118399 | -1.8757364576287165 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].own_markout_5s_bp | -1.8209926138709793 | -1.826531513714097 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].paced_spells | 5489.8 | 1592.6 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].paced_time_share | 0.0121712162448623 | 0.003578428264200746 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].quote_presence_ask | 0.6100162107082928 | 0.7827945102855332 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].quote_presence_bid | 0.60713050465246 | 0.7874512321627759 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].quote_presence_both | 0.32500373735836574 | 0.6091211681049271 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].turnover_per_hour | 153403.67574002955 | 39722.79733979609 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].tw_abs_inventory_avg | 5.944278048143927 | 5.786794472680201 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].fill_rate | 0.2922732735255555 | 0.19899277128228748 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].gate_active_share | 0.5747566764372011 | 0.25478951909896486 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].gross_bp_per_notional | -1.8761399299780515 | -1.908683799302582 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].gross_per_hour | -28.24158102676596 | -7.4354443449602625 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].inc_es | 10.969074589552815 | 4.625669511988081 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].inc_std | 2.613270983756962 | 1.2276716756273665 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].inc_worst | -17.460410750143318 | -6.942793562819654 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].liquidation_shortfall | 0.48130000000000717 | 0.0 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].max_abs_inventory | 10.459500000000098 | 10.06020000000008 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].max_drawdown | 983.5539778425591 | 283.4622409955974 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].net_bp_per_notional | -2.9779676486307247 | -3.0148919756077603 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].net_per_hour | -45.14830381484046 | -11.82211396870709 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].net_per_hour_over_inc_std | -14.89869509176253 | -8.924512694859214 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].orders_per_fill | 0.5113426638028106 | 0.961967467174374 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].own_edge_bp | 0.342297558327605 | 0.5098615739335679 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].own_markout_1s_bp | -1.6260853772700503 | -1.6481554750929877 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].own_markout_30s_bp | -1.910112942118399 | -1.8757364576287165 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].own_markout_5s_bp | -1.8209926138709793 | -1.826531513714097 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].paced_spells | 5489.8 | 1592.6 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].paced_time_share | 0.0121712162448623 | 0.003578428264200746 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].quote_presence_ask | 0.6100162107082928 | 0.7827945102855332 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].quote_presence_bid | 0.60713050465246 | 0.7874512321627759 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].quote_presence_both | 0.32500373735836574 | 0.6091211681049271 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].turnover_per_hour | 153403.67574002955 | 39722.79733979609 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].tw_abs_inventory_avg | 5.944278048143927 | 5.786794472680201 |
| descriptive.scenarios[P3_negM2/conservative/tokyo/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].fill_rate | 0.31961953979271873 | 0.27077569480842484 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].gate_active_share | 0.5751797624796713 | 0.2580492287349659 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].gross_bp_per_notional | -1.5440954799331537 | -1.4516584274102227 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].gross_per_hour | -17.708895124449747 | -6.412339776593251 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].inc_es | 5.941273453239188 | 2.9749177624532073 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].inc_std | 1.923034038344205 | 0.9711272842834656 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].inc_worst | -11.699817787599592 | -4.947806822239338 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].liquidation_shortfall | 0.5451000000000039 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].max_abs_inventory | 10.699899999999824 | 10.566600000000097 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].max_drawdown | 196.60497837555687 | 73.59434593314467 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].net_bp_per_notional | -0.7464076144082988 | -0.6567184388430153 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].net_per_hour | -8.657184272080512 | -2.8767701888774395 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].net_per_hour_over_inc_std | -3.9766134694462343 | -2.7967759821357903 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].orders_per_fill | 0.6553839083829196 | 0.9782241077618543 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].own_edge_bp | 0.2576288011116154 | 0.3413241324252495 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].own_markout_1s_bp | -1.1660862248308768 | -1.1492171682508254 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].own_markout_30s_bp | -1.5009018853733314 | -1.434204813173362 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].own_markout_5s_bp | -1.3778103270770057 | -1.357374117924938 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].paced_spells | 5041.9 | 1661.0 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].paced_time_share | 0.010907552462990225 | 0.0036433087598727403 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].quote_presence_ask | 0.589260609062968 | 0.7828490165605365 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].quote_presence_bid | 0.6145713275316299 | 0.7778301491488702 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].quote_presence_both | 0.3446754489970403 | 0.6183707668525773 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].turnover_per_hour | 113503.06553162404 | 44409.14555862694 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].tw_abs_inventory_avg | 5.530351668766831 | 5.597456273172902 |
| descriptive.scenarios[P3_negM2/intermediate/distant/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].fill_rate | 0.31961953979271873 | 0.27077569480842484 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].gate_active_share | 0.5751797624796713 | 0.2580492287349659 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].gross_bp_per_notional | -1.5440954799331537 | -1.4516584274102227 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].gross_per_hour | -17.708895124449747 | -6.412339776593251 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].inc_es | 22.17405713761098 | 11.828810220133544 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].inc_std | 4.522586457472201 | 2.6334127215336016 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].inc_worst | -30.118736063998863 | -16.019057454000052 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].liquidation_shortfall | 0.5451000000000039 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].max_abs_inventory | 10.699899999999824 | 10.566600000000097 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].max_drawdown | 2883.093890491746 | 1218.8229891300293 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].net_bp_per_notional | -11.554148238520742 | -11.473658477118017 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].net_per_hour | -131.33602322198982 | -50.89610297423907 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].net_per_hour_over_inc_std | -26.042527330087854 | -18.202403139699562 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].orders_per_fill | 0.6553839083829196 | 0.9782241077618543 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].own_edge_bp | 0.2576288011116154 | 0.3413241324252495 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].own_markout_1s_bp | -1.1660862248308768 | -1.1492171682508254 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].own_markout_30s_bp | -1.5009018853733314 | -1.434204813173362 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].own_markout_5s_bp | -1.3778103270770057 | -1.357374117924938 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].paced_spells | 5041.9 | 1661.0 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].paced_time_share | 0.010907552462990225 | 0.0036433087598727403 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].quote_presence_ask | 0.589260609062968 | 0.7828490165605365 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].quote_presence_bid | 0.6145713275316299 | 0.7778301491488702 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].quote_presence_both | 0.3446754489970403 | 0.6183707668525773 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].turnover_per_hour | 113503.06553162404 | 44409.14555862694 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].tw_abs_inventory_avg | 5.530351668766831 | 5.597456273172902 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].fill_rate | 0.31961953979271873 | 0.27077569480842484 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].gate_active_share | 0.5751797624796713 | 0.2580492287349659 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].gross_bp_per_notional | -1.5440954799331537 | -1.4516584274102227 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].gross_per_hour | -17.708895124449747 | -6.412339776593251 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].inc_es | 8.349496000831692 | 4.189842918454759 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].inc_std | 2.0820567357793687 | 1.109872732142366 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].inc_worst | -14.6729690347494 | -6.398859506699999 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].liquidation_shortfall | 0.5451000000000039 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].max_abs_inventory | 10.699899999999824 | 10.566600000000097 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].max_drawdown | 665.8270885705837 | 271.33996671303254 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].net_bp_per_notional | -2.6464076144082993 | -2.5567184388430153 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].net_per_hour | -30.22276672308908 | -11.314507845016557 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].net_per_hour_over_inc_std | -12.979101428503531 | -9.558299491634301 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].orders_per_fill | 0.6553839083829196 | 0.9782241077618543 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].own_edge_bp | 0.2576288011116154 | 0.3413241324252495 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].own_markout_1s_bp | -1.1660862248308768 | -1.1492171682508254 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].own_markout_30s_bp | -1.5009018853733314 | -1.434204813173362 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].own_markout_5s_bp | -1.3778103270770057 | -1.357374117924938 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].paced_spells | 5041.9 | 1661.0 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].paced_time_share | 0.010907552462990225 | 0.0036433087598727403 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].quote_presence_ask | 0.589260609062968 | 0.7828490165605365 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].quote_presence_bid | 0.6145713275316299 | 0.7778301491488702 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].quote_presence_both | 0.3446754489970403 | 0.6183707668525773 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].turnover_per_hour | 113503.06553162404 | 44409.14555862694 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].tw_abs_inventory_avg | 5.530351668766831 | 5.597456273172902 |
| descriptive.scenarios[P3_negM2/intermediate/distant/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].fill_rate | 0.32949217225737565 | 0.26705894514553796 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].gate_active_share | 0.584772784411946 | 0.26191825606817815 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].gross_bp_per_notional | -1.5819451039669445 | -1.4767915889186543 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].gross_per_hour | -25.25274831060537 | -7.496906905421737 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].inc_es | 6.634964705634599 | 3.181339657140872 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].inc_std | 2.011017736115043 | 1.0001878221812783 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].inc_worst | -13.621284354394316 | -4.849601190719918 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].liquidation_shortfall | 0.45490000000000225 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].max_abs_inventory | 10.88539999999986 | 10.651599999999974 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].max_drawdown | 281.09276389424457 | 85.76112350544399 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].net_bp_per_notional | -0.7837559999206134 | -0.6815897416155641 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].net_per_hour | -12.626007452823849 | -3.4265454107888935 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].net_per_hour_over_inc_std | -5.392345420261433 | -3.225046531780896 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].orders_per_fill | 0.5347578101685752 | 0.8835923134639682 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].own_edge_bp | 0.2116069292937463 | 0.3318801292738397 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].own_markout_1s_bp | -1.2400474560381392 | -1.2022422896924159 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].own_markout_30s_bp | -1.5559107534688024 | -1.4669695951780881 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].own_markout_5s_bp | -1.4385411495261489 | -1.4071919800662915 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].paced_spells | 5615.6 | 1698.2 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].paced_time_share | 0.012386490112823768 | 0.003780061800934694 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].quote_presence_ask | 0.6111852401302502 | 0.7888103853065378 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].quote_presence_bid | 0.6325119526029751 | 0.7893090195793355 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].quote_presence_both | 0.3526597677459244 | 0.6230166730676426 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].turnover_per_hour | 158228.2673655242 | 51110.56409294847 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].tw_abs_inventory_avg | 5.484781677326366 | 5.631805600034868 |
| descriptive.scenarios[P3_negM2/intermediate/regional/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].fill_rate | 0.32949217225737565 | 0.26705894514553796 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].gate_active_share | 0.584772784411946 | 0.26191825606817815 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].gross_bp_per_notional | -1.5819451039669445 | -1.4767915889186543 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].gross_per_hour | -25.25274831060537 | -7.496906905421737 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].inc_es | 32.78674356052783 | 14.28455656253359 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].inc_std | 6.854601654528868 | 3.2258527397022405 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].inc_worst | -45.2610766469882 | -20.821154087999172 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].liquidation_shortfall | 0.45490000000000225 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].max_abs_inventory | 10.88539999999986 | 10.651599999999974 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].max_drawdown | 4006.7351763497636 | 1405.4946753880386 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].net_bp_per_notional | -11.58981856463507 | -11.497653122383479 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].net_per_hour | -183.61806146508792 | -58.687834619252975 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].net_per_hour_over_inc_std | -23.9324427343929 | -17.103687196353203 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].orders_per_fill | 0.5347578101685752 | 0.8835923134639682 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].own_edge_bp | 0.2116069292937463 | 0.3318801292738397 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].own_markout_1s_bp | -1.2400474560381392 | -1.2022422896924159 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].own_markout_30s_bp | -1.5559107534688024 | -1.4669695951780881 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].own_markout_5s_bp | -1.4385411495261489 | -1.4071919800662915 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].paced_spells | 5615.6 | 1698.2 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].paced_time_share | 0.012386490112823768 | 0.003780061800934694 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].quote_presence_ask | 0.6111852401302502 | 0.7888103853065378 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].quote_presence_bid | 0.6325119526029751 | 0.7893090195793355 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].quote_presence_both | 0.3526597677459244 | 0.6230166730676426 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].turnover_per_hour | 158228.2673655242 | 51110.56409294847 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].tw_abs_inventory_avg | 5.484781677326366 | 5.631805600034868 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].fill_rate | 0.32949217225737565 | 0.26705894514553796 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].gate_active_share | 0.584772784411946 | 0.26191825606817815 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].gross_bp_per_notional | -1.5819451039669445 | -1.4767915889186543 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].gross_per_hour | -25.25274831060537 | -7.496906905421737 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].inc_es | 10.617874094767284 | 4.780114422744996 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].inc_std | 2.4794688003637675 | 1.2162168155164594 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].inc_worst | -18.751493903454513 | -6.702960636219179 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].liquidation_shortfall | 0.45490000000000225 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].max_abs_inventory | 10.88539999999986 | 10.651599999999974 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].max_drawdown | 933.7587003883339 | 314.8696139537496 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].net_bp_per_notional | -2.6837559999206135 | -2.581589741615564 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].net_per_hour | -42.68937825227344 | -13.137552588449102 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].net_per_hour_over_inc_std | -15.05948730225787 | -10.098203283968937 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].orders_per_fill | 0.5347578101685752 | 0.8835923134639682 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].own_edge_bp | 0.2116069292937463 | 0.3318801292738397 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].own_markout_1s_bp | -1.2400474560381392 | -1.2022422896924159 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].own_markout_30s_bp | -1.5559107534688024 | -1.4669695951780881 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].own_markout_5s_bp | -1.4385411495261489 | -1.4071919800662915 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].paced_spells | 5615.6 | 1698.2 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].paced_time_share | 0.012386490112823768 | 0.003780061800934694 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].quote_presence_ask | 0.6111852401302502 | 0.7888103853065378 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].quote_presence_bid | 0.6325119526029751 | 0.7893090195793355 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].quote_presence_both | 0.3526597677459244 | 0.6230166730676426 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].turnover_per_hour | 158228.2673655242 | 51110.56409294847 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].tw_abs_inventory_avg | 5.484781677326366 | 5.631805600034868 |
| descriptive.scenarios[P3_negM2/intermediate/regional/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].fill_rate | 0.3369477741284609 | 0.25403727028677975 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].gate_active_share | 0.5848559384167669 | 0.2637996822259483 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].gross_bp_per_notional | -1.7432777907216246 | -1.636332435887835 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].gross_per_hour | -31.203420421241 | -8.701965487746724 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].inc_es | 6.893718492761972 | 3.316852718570735 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].inc_std | 2.0404849388086648 | 1.034342204252473 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].inc_worst | -12.506907732759627 | -5.231446808160951 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].liquidation_shortfall | 0.5247000000000058 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].max_abs_inventory | 10.342300000000131 | 9.995400000000028 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].max_drawdown | 370.680712949503 | 108.21160752972362 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].net_bp_per_notional | -0.9447728702323911 | -0.8412924750351264 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].net_per_hour | -16.793124864518923 | -4.435473483712785 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].net_per_hour_over_inc_std | -7.190907682738114 | -4.042229093738242 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].orders_per_fill | 0.4974002634826279 | 0.8833033228190541 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].own_edge_bp | 0.3551635614646521 | 0.5276611941018772 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].own_markout_1s_bp | -1.4314913479178317 | -1.3694873002387395 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].own_markout_30s_bp | -1.7300584578630591 | -1.612347219079485 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].own_markout_5s_bp | -1.628897540550953 | -1.56482908309147 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].paced_spells | 5926.2 | 1864.4 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].paced_time_share | 0.013216365209431652 | 0.004192761271392802 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].quote_presence_ask | 0.6115404252954605 | 0.7951410550701555 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].quote_presence_bid | 0.6129856705868535 | 0.7848628254316665 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].quote_presence_both | 0.33538624650801535 | 0.622521014300194 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].turnover_per_hour | 180543.37627748869 | 53573.886642131256 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].tw_abs_inventory_avg | 5.753631412533034 | 5.543967025237627 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].fill_rate | 0.3369477741284609 | 0.25403727028677975 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].gate_active_share | 0.5848559384167669 | 0.2637996822259483 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].gross_bp_per_notional | -1.7432777907216246 | -1.636332435887835 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].gross_per_hour | -31.203420421241 | -8.701965487746724 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].inc_es | 36.187575491694155 | 14.592746434400661 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].inc_std | 7.561867063083703 | 3.311114090977058 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].inc_worst | -46.619790092993966 | -20.676440540001103 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].liquidation_shortfall | 0.5247000000000058 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].max_abs_inventory | 10.342300000000131 | 9.995400000000028 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].max_drawdown | 4613.213295905738 | 1493.580527236036 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].net_bp_per_notional | -11.74977813642061 | -11.657897823484754 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].net_per_hour | -211.8910338529776 | -62.36028224873259 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].net_per_hour_over_inc_std | -25.014023165339708 | -17.634301309076637 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].orders_per_fill | 0.4974002634826279 | 0.8833033228190541 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].own_edge_bp | 0.3551635614646521 | 0.5276611941018772 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].own_markout_1s_bp | -1.4314913479178317 | -1.3694873002387395 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].own_markout_30s_bp | -1.7300584578630591 | -1.612347219079485 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].own_markout_5s_bp | -1.628897540550953 | -1.56482908309147 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].paced_spells | 5926.2 | 1864.4 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].paced_time_share | 0.013216365209431652 | 0.004192761271392802 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].quote_presence_ask | 0.6115404252954605 | 0.7951410550701555 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].quote_presence_bid | 0.6129856705868535 | 0.7848628254316665 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].quote_presence_both | 0.33538624650801535 | 0.622521014300194 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].turnover_per_hour | 180543.37627748869 | 53573.886642131256 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].tw_abs_inventory_avg | 5.753631412533034 | 5.543967025237627 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].fill_rate | 0.3369477741284609 | 0.25403727028677975 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].gate_active_share | 0.5848559384167669 | 0.2637996822259483 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].gross_bp_per_notional | -1.7432777907216246 | -1.636332435887835 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].gross_per_hour | -31.203420421241 | -8.701965487746724 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].inc_es | 11.37949540604819 | 4.969153557566822 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].inc_std | 2.6183728766538152 | 1.255353530383584 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].inc_worst | -17.44410995801652 | -7.300445281899643 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].liquidation_shortfall | 0.5247000000000058 | 0.0 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].max_abs_inventory | 10.342300000000131 | 9.995400000000028 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].max_drawdown | 1115.6995962645774 | 350.1016117017686 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].net_bp_per_notional | -2.844772870232391 | -2.7412924750351264 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].net_per_hour | -51.09636635724177 | -14.614511945717723 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].net_per_hour_over_inc_std | -17.06926173238931 | -10.865162588484756 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].orders_per_fill | 0.4974002634826279 | 0.8833033228190541 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].own_edge_bp | 0.3551635614646521 | 0.5276611941018772 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].own_markout_1s_bp | -1.4314913479178317 | -1.3694873002387395 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].own_markout_30s_bp | -1.7300584578630591 | -1.612347219079485 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].own_markout_5s_bp | -1.628897540550953 | -1.56482908309147 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].paced_spells | 5926.2 | 1864.4 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].paced_time_share | 0.013216365209431652 | 0.004192761271392802 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].quote_presence_ask | 0.6115404252954605 | 0.7951410550701555 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].quote_presence_bid | 0.6129856705868535 | 0.7848628254316665 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].quote_presence_both | 0.33538624650801535 | 0.622521014300194 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].turnover_per_hour | 180543.37627748869 | 53573.886642131256 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].tw_abs_inventory_avg | 5.753631412533034 | 5.543967025237627 |
| descriptive.scenarios[P3_negM2/intermediate/tokyo/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].fill_rate | 0.4522247945682646 | 0.43830750607272595 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].gate_active_share | 0.5742951205163938 | 0.2651703395562942 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].gross_bp_per_notional | -1.2459924217226153 | -1.0384535641096502 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].gross_per_hour | -20.511786133846194 | -7.966473806116596 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].inc_es | 5.7710280766490785 | 2.776020321504177 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].inc_std | 1.9433557896585196 | 0.9492863506277607 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].inc_worst | -12.253267222920059 | -4.7531986611194155 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].liquidation_shortfall | 0.5400000000000011 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].max_abs_inventory | 10.353900000000039 | 10.300200000000036 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].max_drawdown | 179.39881575271028 | 52.60746433929826 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].net_bp_per_notional | -0.4476089648358835 | -0.24104103436856822 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].net_per_hour | -7.9121418082306265 | -1.9210347253512836 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].net_per_hour_over_inc_std | -3.4628840430343097 | -1.8808553960403949 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].orders_per_fill | 0.5977534091788048 | 0.8140189910838821 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].own_edge_bp | 0.41453763050026404 | 0.5792450199941459 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].own_markout_1s_bp | -0.8578038001616581 | -0.7773224199970058 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].own_markout_30s_bp | -1.19543029063108 | -1.0641866364392258 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].own_markout_5s_bp | -1.0755434245160802 | -0.9938223717853727 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].paced_spells | 6420.7 | 2451.8 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].paced_time_share | 0.014332105503589706 | 0.0055720114366833206 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].quote_presence_ask | 0.5606978640453901 | 0.7713165906999805 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].quote_presence_bid | 0.6025783817635118 | 0.7615739791372065 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].quote_presence_both | 0.33510891312191726 | 0.6062741355362935 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].turnover_per_hour | 157862.96028843668 | 75780.57541624646 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].tw_abs_inventory_avg | 5.475536025974405 | 5.440306108842155 |
| descriptive.scenarios[P3_negM2/optimistic/distant/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].fill_rate | 0.4522247945682646 | 0.43830750607272595 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].gate_active_share | 0.5742951205163938 | 0.2651703395562942 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].gross_bp_per_notional | -1.2459924217226153 | -1.0384535641096502 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].gross_per_hour | -20.511786133846194 | -7.966473806116596 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].inc_es | 27.068140329979986 | 16.976506135333203 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].inc_std | 5.318366047418062 | 3.6456245377648004 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].inc_worst | -34.59293087399534 | -21.722460542001084 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].liquidation_shortfall | 0.5400000000000011 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].max_abs_inventory | 10.353900000000039 | 10.300200000000036 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].max_drawdown | 3937.705953834963 | 2006.8144225999845 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].net_bp_per_notional | -11.253020870041173 | -11.0497034348006 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].net_per_hour | -178.50253988949754 | -83.82099249425178 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].net_per_hour_over_inc_std | -30.75490511648247 | -21.760349531079285 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].orders_per_fill | 0.5977534091788048 | 0.8140189910838821 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].own_edge_bp | 0.41453763050026404 | 0.5792450199941459 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].own_markout_1s_bp | -0.8578038001616581 | -0.7773224199970058 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].own_markout_30s_bp | -1.19543029063108 | -1.0641866364392258 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].own_markout_5s_bp | -1.0755434245160802 | -0.9938223717853727 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].paced_spells | 6420.7 | 2451.8 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].paced_time_share | 0.014332105503589706 | 0.0055720114366833206 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].quote_presence_ask | 0.5606978640453901 | 0.7713165906999805 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].quote_presence_bid | 0.6025783817635118 | 0.7615739791372065 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].quote_presence_both | 0.33510891312191726 | 0.6062741355362935 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].turnover_per_hour | 157862.96028843668 | 75780.57541624646 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].tw_abs_inventory_avg | 5.475536025974405 | 5.440306108842155 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].fill_rate | 0.4522247945682646 | 0.43830750607272595 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].gate_active_share | 0.5742951205163938 | 0.2651703395562942 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].gross_bp_per_notional | -1.2459924217226153 | -1.0384535641096502 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].gross_per_hour | -20.511786133846194 | -7.966473806116596 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].inc_es | 9.009104761132722 | 4.7919373769973275 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].inc_std | 2.1597851821855056 | 1.180413611564469 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].inc_worst | -15.795211338759533 | -7.18069141286018 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].liquidation_shortfall | 0.5400000000000011 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].max_abs_inventory | 10.353900000000039 | 10.300200000000036 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].max_drawdown | 837.1447614542978 | 390.9151932271812 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].net_bp_per_notional | -2.3476089648358833 | -2.1410410343685684 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].net_per_hour | -37.9061042630336 | -16.319344054438112 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].net_per_hour_over_inc_std | -15.965287999640775 | -12.95557989407653 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].orders_per_fill | 0.5977534091788048 | 0.8140189910838821 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].own_edge_bp | 0.41453763050026404 | 0.5792450199941459 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].own_markout_1s_bp | -0.8578038001616581 | -0.7773224199970058 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].own_markout_30s_bp | -1.19543029063108 | -1.0641866364392258 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].own_markout_5s_bp | -1.0755434245160802 | -0.9938223717853727 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].paced_spells | 6420.7 | 2451.8 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].paced_time_share | 0.014332105503589706 | 0.0055720114366833206 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].quote_presence_ask | 0.5606978640453901 | 0.7713165906999805 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].quote_presence_bid | 0.6025783817635118 | 0.7615739791372065 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].quote_presence_both | 0.33510891312191726 | 0.6062741355362935 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].turnover_per_hour | 157862.96028843668 | 75780.57541624646 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].tw_abs_inventory_avg | 5.475536025974405 | 5.440306108842155 |
| descriptive.scenarios[P3_negM2/optimistic/distant/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].fill_rate | 0.5664608407008671 | 0.5197150633799958 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].gate_active_share | 0.5832905748057509 | 0.27432611193727985 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].gross_bp_per_notional | -1.2918057528267073 | -1.1237328847022467 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].gross_per_hour | -34.94980922602214 | -12.116260450737826 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].inc_es | 6.715871596551862 | 3.0343099828480162 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].inc_std | 2.0470845357937852 | 0.9864986401754907 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].inc_worst | -13.353427790156573 | -5.531185003679434 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].liquidation_shortfall | 0.4485000000000019 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].max_abs_inventory | 10.309000000000307 | 10.306000000000001 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].max_drawdown | 308.4217087549913 | 92.88556400252776 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].net_bp_per_notional | -0.49296544494065264 | -0.3259744733133248 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].net_per_hour | -13.967982939259278 | -3.65782834622503 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].net_per_hour_over_inc_std | -5.811387211366022 | -3.423505331845152 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].orders_per_fill | 0.5047828084932893 | 0.7170421546263822 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].own_edge_bp | 0.41171387180944585 | 0.5774235888883199 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].own_markout_1s_bp | -0.9476172907936169 | -0.8677593103953196 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].own_markout_30s_bp | -1.2539293994238097 | -1.1303594355318833 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].own_markout_5s_bp | -1.1464358901173346 | -1.0810688512904387 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].paced_spells | 8876.6 | 3051.8 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].paced_time_share | 0.02050027395857187 | 0.0070688995966176225 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].quote_presence_ask | 0.577609537119325 | 0.7820511167436617 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].quote_presence_bid | 0.6141894804150988 | 0.7719073147821154 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].quote_presence_both | 0.340690805876836 | 0.6145758615818819 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].turnover_per_hour | 262696.91736764787 | 105950.54042700873 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].tw_abs_inventory_avg | 5.444069833046143 | 5.448815694833592 |
| descriptive.scenarios[P3_negM2/optimistic/regional/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].fill_rate | 0.5664608407008671 | 0.5197150633799958 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].gate_active_share | 0.5832905748057509 | 0.27432611193727985 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].gross_bp_per_notional | -1.2918057528267073 | -1.1237328847022467 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].gross_per_hour | -34.94980922602214 | -12.116260450737826 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].inc_es | 45.93079748462419 | 24.744992053465293 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].inc_std | 9.188047902535336 | 5.432270408206888 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].inc_worst | -58.71706816299005 | -30.870776932001263 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].liquidation_shortfall | 0.4485000000000019 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].max_abs_inventory | 10.309000000000307 | 10.306000000000001 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].max_drawdown | 6528.498629137833 | 2828.6388099579026 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].net_bp_per_notional | -11.296847892452556 | -11.133478922141716 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].net_per_hour | -297.794235735622 | -118.14337100665048 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].net_per_hour_over_inc_std | -29.221011519840097 | -20.623498914204305 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].orders_per_fill | 0.5047828084932893 | 0.7170421546263822 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].own_edge_bp | 0.41171387180944585 | 0.5774235888883199 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].own_markout_1s_bp | -0.9476172907936169 | -0.8677593103953196 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].own_markout_30s_bp | -1.2539293994238097 | -1.1303594355318833 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].own_markout_5s_bp | -1.1464358901173346 | -1.0810688512904387 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].paced_spells | 8876.6 | 3051.8 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].paced_time_share | 0.02050027395857187 | 0.0070688995966176225 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].quote_presence_ask | 0.577609537119325 | 0.7820511167436617 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].quote_presence_bid | 0.6141894804150988 | 0.7719073147821154 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].quote_presence_both | 0.340690805876836 | 0.6145758615818819 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].turnover_per_hour | 262696.91736764787 | 105950.54042700873 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].tw_abs_inventory_avg | 5.444069833046143 | 5.448815694833592 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].fill_rate | 0.5664608407008671 | 0.5197150633799958 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].gate_active_share | 0.5832905748057509 | 0.27432611193727985 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].gross_bp_per_notional | -1.2918057528267073 | -1.1237328847022467 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].gross_per_hour | -34.94980922602214 | -12.116260450737826 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].inc_es | 12.902040654774945 | 6.3239053961826315 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].inc_std | 2.78360715179897 | 1.4988565945252366 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].inc_worst | -20.714444301766903 | -9.086291089379275 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].liquidation_shortfall | 0.4485000000000019 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].max_abs_inventory | 10.309000000000307 | 10.306000000000001 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].max_drawdown | 1400.833353994542 | 569.6013536117509 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].net_bp_per_notional | -2.3929654449406526 | -2.2259744733133244 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].net_per_hour | -63.88039723911238 | -23.788431027356687 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].net_per_hour_over_inc_std | -20.378425255440654 | -14.823241879786377 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].orders_per_fill | 0.5047828084932893 | 0.7170421546263822 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].own_edge_bp | 0.41171387180944585 | 0.5774235888883199 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].own_markout_1s_bp | -0.9476172907936169 | -0.8677593103953196 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].own_markout_30s_bp | -1.2539293994238097 | -1.1303594355318833 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].own_markout_5s_bp | -1.1464358901173346 | -1.0810688512904387 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].paced_spells | 8876.6 | 3051.8 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].paced_time_share | 0.02050027395857187 | 0.0070688995966176225 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].quote_presence_ask | 0.577609537119325 | 0.7820511167436617 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].quote_presence_bid | 0.6141894804150988 | 0.7719073147821154 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].quote_presence_both | 0.340690805876836 | 0.6145758615818819 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].turnover_per_hour | 262696.91736764787 | 105950.54042700873 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].tw_abs_inventory_avg | 5.444069833046143 | 5.448815694833592 |
| descriptive.scenarios[P3_negM2/optimistic/regional/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].fill_rate | 0.6174403367245827 | 0.5681628285778209 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].gate_active_share | 0.5913722539772016 | 0.28194342025352215 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].gross_bp_per_notional | -1.456313132360874 | -1.3103553034918163 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].gross_per_hour | -48.01737883434592 | -17.215081930531966 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].inc_es | 7.5449881392694085 | 3.59406505758957 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].inc_std | 2.1350582960581987 | 1.0822034834787122 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].inc_worst | -13.214984916559084 | -5.6797880855996095 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].liquidation_shortfall | 0.4549000000000015 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].max_abs_inventory | 10.130899999999965 | 10.000000000000004 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].max_drawdown | 484.07821799737746 | 167.36271773153732 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].net_bp_per_notional | -0.6571693483223474 | -0.5120855024876004 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].net_per_hour | -21.96471187577663 | -6.862910596361834 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].net_per_hour_over_inc_std | -9.052810103235618 | -5.854742278014681 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].orders_per_fill | 0.39557225009286406 | 0.5695984104751025 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].own_edge_bp | 0.41126839669465076 | 0.5771479149631953 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].own_markout_1s_bp | -1.1295533965019975 | -1.043916616529188 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].own_markout_30s_bp | -1.4241500120031296 | -1.2898553209967933 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].own_markout_5s_bp | -1.3267491148170443 | -1.2455826176990998 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].paced_spells | 7715.5 | 2535.6 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].paced_time_share | 0.017427819055979756 | 0.005752883000782236 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].quote_presence_ask | 0.586378850471937 | 0.7824535391231737 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].quote_presence_bid | 0.6080037353178505 | 0.7752708960239745 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].quote_presence_both | 0.33260543945879906 | 0.6113267157213659 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].turnover_per_hour | 326067.5290682358 | 129607.18003211865 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].tw_abs_inventory_avg | 5.613421942549737 | 5.464666425327481 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/lp_tier4].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].fill_rate | 0.6174403367245827 | 0.5681628285778209 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].gate_active_share | 0.5913722539772016 | 0.28194342025352215 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].gross_bp_per_notional | -1.456313132360874 | -1.3103553034918163 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].gross_per_hour | -48.01737883434592 | -17.215081930531966 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].inc_es | 55.57507035526068 | 30.436113194132737 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].inc_std | 11.418430701151845 | 6.751439775552493 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].inc_worst | -66.65562905999884 | -37.34188022199862 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].liquidation_shortfall | 0.4549000000000015 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].max_abs_inventory | 10.130899999999965 | 10.000000000000004 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].max_drawdown | 8207.206699075708 | 3517.295973489905 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].net_bp_per_notional | -11.460035810454237 | -11.317877907821313 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].net_per_hour | -374.22723558471023 | -146.89357965134346 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].net_per_hour_over_inc_std | -29.648264476975726 | -20.612913605975315 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].orders_per_fill | 0.39557225009286406 | 0.5695984104751025 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].own_edge_bp | 0.41126839669465076 | 0.5771479149631953 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].own_markout_1s_bp | -1.1295533965019975 | -1.043916616529188 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].own_markout_30s_bp | -1.4241500120031296 | -1.2898553209967933 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].own_markout_5s_bp | -1.3267491148170443 | -1.2455826176990998 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].paced_spells | 7715.5 | 2535.6 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].paced_time_share | 0.017427819055979756 | 0.005752883000782236 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].quote_presence_ask | 0.586378850471937 | 0.7824535391231737 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].quote_presence_bid | 0.6080037353178505 | 0.7752708960239745 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].quote_presence_both | 0.33260543945879906 | 0.6113267157213659 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].turnover_per_hour | 326067.5290682358 | 129607.18003211865 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].tw_abs_inventory_avg | 5.613421942549737 | 5.464666425327481 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip0].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].fill_rate | 0.6174403367245827 | 0.5681628285778209 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].gate_active_share | 0.5913722539772016 | 0.28194342025352215 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].gross_bp_per_notional | -1.456313132360874 | -1.3103553034918163 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].gross_per_hour | -48.01737883434592 | -17.215081930531966 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].inc_es | 15.12507857771313 | 7.7983559866572465 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].inc_std | 3.224994271419771 | 1.8183203999031465 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].inc_worst | -21.586938789839543 | -10.410810805519054 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].liquidation_shortfall | 0.4549000000000015 | 0.0 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].max_abs_inventory | 10.130899999999965 | 10.000000000000004 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].max_drawdown | 1841.640423983023 | 754.0187266738624 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].net_bp_per_notional | -2.557169348322348 | -2.4120855024876007 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].net_per_hour | -83.91754239874143 | -31.488274802464378 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].net_per_hour_over_inc_std | -23.094070985968877 | -16.200429653215586 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].orders_per_fill | 0.39557225009286406 | 0.5695984104751025 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].own_edge_bp | 0.41126839669465076 | 0.5771479149631953 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].own_markout_1s_bp | -1.1295533965019975 | -1.043916616529188 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].own_markout_30s_bp | -1.4241500120031296 | -1.2898553209967933 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].own_markout_5s_bp | -1.3267491148170443 | -1.2455826176990998 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].paced_spells | 7715.5 | 2535.6 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].paced_time_share | 0.017427819055979756 | 0.005752883000782236 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].quote_presence_ask | 0.586378850471937 | 0.7824535391231737 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].quote_presence_bid | 0.6080037353178505 | 0.7752708960239745 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].quote_presence_both | 0.33260543945879906 | 0.6113267157213659 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].turnover_per_hour | 326067.5290682358 | 129607.18003211865 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].tw_abs_inventory_avg | 5.613421942549737 | 5.464666425327481 |
| descriptive.scenarios[P3_negM2/optimistic/tokyo/vip9].vol_closed_share | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].fill_rate | 0.24478493458074277 | 0.22299197683524957 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].gate_active_share | 0.07662188529984745 | 0.02981960283866763 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].gross_bp_per_notional | -1.644192627807822 | -1.6315549810454133 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].gross_per_hour | -15.364992387849762 | -5.234991948160274 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].inc_es | 2.5527156210908375 | 1.231198238613267 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].inc_std | 0.700634447252223 | 0.3654892129407685 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].inc_worst | -4.1035220106006305 | -2.254320481600003 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].max_abs_inventory | 4.508399999999989 | 4.5992000000000015 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].max_drawdown | 175.86454466512262 | 63.44523759257646 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].net_bp_per_notional | -0.8454135872150278 | -0.8351711480483995 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].net_per_hour | -7.973825324232751 | -2.6383539761535513 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].net_per_hour_over_inc_std | -9.787461072627078 | -6.726392901633884 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].orders_per_fill | 0.612486747354757 | 0.9026099785348324 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].own_edge_bp | 0.19490864269282868 | 0.21228923046338113 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].own_markout_1s_bp | -1.3355726899601066 | -1.4046478564193614 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].own_markout_30s_bp | -1.6313054861740155 | -1.6312575495289328 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].own_markout_5s_bp | -1.5326956462571302 | -1.597282500315179 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].paced_spells | 2783.8 | 418.4 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].paced_time_share | 0.008016627545811481 | 0.00112061242934727 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].quote_presence_ask | 0.8143001942806636 | 0.8351894172870942 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].quote_presence_bid | 0.8190270389066592 | 0.8652726978859082 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].quote_presence_both | 0.6801880157276863 | 0.7205043685209949 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].turnover_per_hour | 92524.36540143484 | 32553.518672932558 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].tw_abs_inventory_avg | 1.8310373361321894 | 1.9369590542592632 |
| descriptive.scenarios[P4/conservative/distant/lp_tier4].vol_closed_share | 0.031355930250187194 | 0.015309545281198553 |
| descriptive.scenarios[P4/conservative/distant/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P4/conservative/distant/vip0].gate_active_share | 0.9620679298503891 | 0.983257015776277 |
| descriptive.scenarios[P4/conservative/distant/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/conservative/distant/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/conservative/distant/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P4/conservative/distant/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P4/conservative/distant/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P4/conservative/distant/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P4/conservative/distant/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P4/conservative/distant/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P4/conservative/distant/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P4/conservative/distant/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip0].vol_closed_share | 0.03793207014961088 | 0.016742984223722994 |
| descriptive.scenarios[P4/conservative/distant/vip9].fill_rate | 0.014804104404936217 | 0.013051706188697101 |
| descriptive.scenarios[P4/conservative/distant/vip9].gate_active_share | 0.9623100966087739 | 0.9833502981158503 |
| descriptive.scenarios[P4/conservative/distant/vip9].gross_bp_per_notional | -1.3104629247351391 | -1.8282094523854902 |
| descriptive.scenarios[P4/conservative/distant/vip9].gross_per_hour | -0.6334902686339494 | -0.27239681205119165 |
| descriptive.scenarios[P4/conservative/distant/vip9].inc_es | 0.8313330069544778 | 0.38680022210266907 |
| descriptive.scenarios[P4/conservative/distant/vip9].inc_std | 0.2851501858395645 | 0.1176399233864788 |
| descriptive.scenarios[P4/conservative/distant/vip9].inc_worst | -1.6683553197400478 | -0.8291557771799845 |
| descriptive.scenarios[P4/conservative/distant/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip9].max_abs_inventory | 2.5321999999999996 | 2.3136 |
| descriptive.scenarios[P4/conservative/distant/vip9].max_drawdown | 24.85616730060017 | 10.378655617300065 |
| descriptive.scenarios[P4/conservative/distant/vip9].net_bp_per_notional | -2.4221114554745578 | -2.943136064575225 |
| descriptive.scenarios[P4/conservative/distant/vip9].net_per_hour | -1.0449683329719328 | -0.4185661502472725 |
| descriptive.scenarios[P4/conservative/distant/vip9].net_per_hour_over_inc_std | -3.1937243169389946 | -3.243741318417599 |
| descriptive.scenarios[P4/conservative/distant/vip9].orders_per_fill | 11.693050069213644 | 13.55420591995296 |
| descriptive.scenarios[P4/conservative/distant/vip9].own_edge_bp | 0.2675905854812741 | 0.24576451242913838 |
| descriptive.scenarios[P4/conservative/distant/vip9].own_markout_1s_bp | -1.7303598401141635 | -1.7686093415792397 |
| descriptive.scenarios[P4/conservative/distant/vip9].own_markout_30s_bp | -1.8599423010225642 | -1.8259818741734093 |
| descriptive.scenarios[P4/conservative/distant/vip9].own_markout_5s_bp | -1.8747528606445425 | -1.7568375465096207 |
| descriptive.scenarios[P4/conservative/distant/vip9].paced_spells | 91.4 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip9].paced_time_share | 0.00014593586155038236 | 0.0 |
| descriptive.scenarios[P4/conservative/distant/vip9].quote_presence_ask | 0.14284913190488105 | 0.13335159208182823 |
| descriptive.scenarios[P4/conservative/distant/vip9].quote_presence_bid | 0.12734225979210775 | 0.14570095223572893 |
| descriptive.scenarios[P4/conservative/distant/vip9].quote_presence_both | 5.918575271322891e-07 | 2.435441348325277e-07 |
| descriptive.scenarios[P4/conservative/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P4/conservative/distant/vip9].turnover_per_hour | 3712.927869983444 | 1315.3493399267404 |
| descriptive.scenarios[P4/conservative/distant/vip9].tw_abs_inventory_avg | 0.6647346227558549 | 0.48074036370674883 |
| descriptive.scenarios[P4/conservative/distant/vip9].vol_closed_share | 0.03753239304302067 | 0.016647978452036628 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].fill_rate | 0.23767691208097333 | 0.20696471801331198 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].gate_active_share | 0.07479283993621776 | 0.030080387038275848 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].gross_bp_per_notional | -1.6748503759288567 | -1.6527853443783354 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].gross_per_hour | -17.379146811721295 | -5.5043989368732085 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].inc_es | 2.624287300147786 | 1.3385542699413542 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].inc_std | 0.7106801628753843 | 0.38910972955353973 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].inc_worst | -3.8832627715205716 | -2.2749870928000133 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].max_abs_inventory | 4.69399999999989 | 4.798399999999977 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].max_drawdown | 199.59661203102982 | 67.42988772993735 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].net_bp_per_notional | -0.875905926555896 | -0.8561824857468026 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].net_per_hour | -9.0848329315096 | -2.8054894847850496 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].net_per_hour_over_inc_std | -11.080125273574028 | -6.709448212888352 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].orders_per_fill | 0.5961166496115302 | 0.9387987814116917 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].own_edge_bp | 0.17948206004448553 | 0.2491058306288775 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].own_markout_1s_bp | -1.3864957152051613 | -1.426531260229286 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].own_markout_30s_bp | -1.6692710697398454 | -1.6659477139827374 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].own_markout_5s_bp | -1.582200032041332 | -1.613465743836161 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].paced_spells | 3250.2 | 487.8 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].paced_time_share | 0.009013403152076941 | 0.0012972721413579858 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].quote_presence_ask | 0.8373992491798573 | 0.8522967502150152 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].quote_presence_bid | 0.8393400569561404 | 0.8787819105383745 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].quote_presence_both | 0.7205083675553953 | 0.7492750802811455 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].turnover_per_hour | 103807.7180348628 | 33828.92066566247 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].tw_abs_inventory_avg | 1.7792785809040794 | 1.9289068503557587 |
| descriptive.scenarios[P4/conservative/regional/lp_tier4].vol_closed_share | 0.03100518685882302 | 0.015346551823877716 |
| descriptive.scenarios[P4/conservative/regional/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P4/conservative/regional/vip0].gate_active_share | 0.9620677937155758 | 0.9832570463064109 |
| descriptive.scenarios[P4/conservative/regional/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/conservative/regional/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/conservative/regional/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P4/conservative/regional/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P4/conservative/regional/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P4/conservative/regional/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P4/conservative/regional/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P4/conservative/regional/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P4/conservative/regional/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P4/conservative/regional/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip0].vol_closed_share | 0.03793220628442419 | 0.016742953693589243 |
| descriptive.scenarios[P4/conservative/regional/vip9].fill_rate | 0.010552442353310485 | 0.009689080171461818 |
| descriptive.scenarios[P4/conservative/regional/vip9].gate_active_share | 0.9621431236667706 | 0.9833117113104082 |
| descriptive.scenarios[P4/conservative/regional/vip9].gross_bp_per_notional | -1.6080573674311232 | -2.0300957344138477 |
| descriptive.scenarios[P4/conservative/regional/vip9].gross_per_hour | -0.4388430838473088 | -0.20418200817088517 |
| descriptive.scenarios[P4/conservative/regional/vip9].inc_es | 0.7901184668347558 | 0.3467127875333308 |
| descriptive.scenarios[P4/conservative/regional/vip9].inc_std | 0.26677578090513604 | 0.11259393622137756 |
| descriptive.scenarios[P4/conservative/regional/vip9].inc_worst | -1.423402962340043 | -0.7269579225799923 |
| descriptive.scenarios[P4/conservative/regional/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip9].max_abs_inventory | 2.6900999999999993 | 2.2099999999999995 |
| descriptive.scenarios[P4/conservative/regional/vip9].max_drawdown | 16.884545279050133 | 8.02950124054001 |
| descriptive.scenarios[P4/conservative/regional/vip9].net_bp_per_notional | -2.7236960119574634 | -3.1474723402083593 |
| descriptive.scenarios[P4/conservative/regional/vip9].net_per_hour | -0.6970152202222646 | -0.3118727088404066 |
| descriptive.scenarios[P4/conservative/regional/vip9].net_per_hour_over_inc_std | -2.536556980952978 | -2.6484187597353483 |
| descriptive.scenarios[P4/conservative/regional/vip9].orders_per_fill | 19.089029591999303 | 22.542118605242724 |
| descriptive.scenarios[P4/conservative/regional/vip9].own_edge_bp | 0.25120262280037775 | 0.3236840578559793 |
| descriptive.scenarios[P4/conservative/regional/vip9].own_markout_1s_bp | -1.9455453592687824 | -1.8285333573789426 |
| descriptive.scenarios[P4/conservative/regional/vip9].own_markout_30s_bp | -1.9650313611878947 | -1.834381752629658 |
| descriptive.scenarios[P4/conservative/regional/vip9].own_markout_5s_bp | -2.0362008831915475 | -1.9637095029883702 |
| descriptive.scenarios[P4/conservative/regional/vip9].paced_spells | 95.5 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip9].paced_time_share | 0.0001527114666492584 | 0.0 |
| descriptive.scenarios[P4/conservative/regional/vip9].quote_presence_ask | 0.1453150216889344 | 0.12886765420164298 |
| descriptive.scenarios[P4/conservative/regional/vip9].quote_presence_bid | 0.1303161345803609 | 0.15133166236647344 |
| descriptive.scenarios[P4/conservative/regional/vip9].quote_presence_both | 6.985877772946069e-07 | 8.137472741390884e-07 |
| descriptive.scenarios[P4/conservative/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P4/conservative/regional/vip9].turnover_per_hour | 2318.1233079341964 | 965.9045373434722 |
| descriptive.scenarios[P4/conservative/regional/vip9].tw_abs_inventory_avg | 0.65660630559966 | 0.4836634707935382 |
| descriptive.scenarios[P4/conservative/regional/vip9].vol_closed_share | 0.03773843545091644 | 0.016684166460106148 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].fill_rate | 0.23356771692682274 | 0.18576448790033676 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].gate_active_share | 0.07446332232640412 | 0.03035652472231547 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].gross_bp_per_notional | -1.8171638750982297 | -1.803856578258874 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].gross_per_hour | -19.34108216737106 | -5.757223340112593 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].inc_es | 2.8590804357592683 | 1.3673106779093642 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].inc_std | 0.7576033939844671 | 0.39948974568799767 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].inc_worst | -4.224902084160902 | -2.406963431840117 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].max_abs_inventory | 4.174900000000155 | 4.1822 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].max_drawdown | 234.4836172229872 | 76.24244824049804 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].net_bp_per_notional | -1.0180493185677182 | -1.0073590053156773 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].net_per_hour | -10.676322778699346 | -3.1720656078611347 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].net_per_hour_over_inc_std | -12.407885283315313 | -7.378321840612115 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].orders_per_fill | 0.6127776240720213 | 1.056704418381025 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].own_edge_bp | 0.3485917291642149 | 0.5180987207203251 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].own_markout_1s_bp | -1.5465385191191576 | -1.567827745912163 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].own_markout_30s_bp | -1.8070104933892914 | -1.8061812048267605 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].own_markout_5s_bp | -1.738288039245461 | -1.7486143101663232 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].paced_spells | 3475.9 | 551.6 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].paced_time_share | 0.009638923108696367 | 0.0014515697036426981 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].quote_presence_ask | 0.8282504603073958 | 0.8587498919662135 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].quote_presence_bid | 0.8234763514515002 | 0.8701316294060814 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].quote_presence_both | 0.6951428681952714 | 0.7467661774982586 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].turnover_per_hour | 108430.56118042178 | 32401.65419868338 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].tw_abs_inventory_avg | 1.87677178630064 | 1.9596613978635709 |
| descriptive.scenarios[P4/conservative/tokyo/lp_tier4].vol_closed_share | 0.0311792177883314 | 0.015420731702022395 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P4/conservative/tokyo/vip0].gate_active_share | 0.9620677704387482 | 0.9832570340571044 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/conservative/tokyo/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/conservative/tokyo/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P4/conservative/tokyo/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P4/conservative/tokyo/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P4/conservative/tokyo/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P4/conservative/tokyo/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P4/conservative/tokyo/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P4/conservative/tokyo/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip0].vol_closed_share | 0.037932229561251765 | 0.01674296594289569 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].fill_rate | 0.008877906626074008 | 0.007783346933016344 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].gate_active_share | 0.9616472913272647 | 0.9832915554505346 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].gross_bp_per_notional | -1.981656669900124 | -2.1225600906877973 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].gross_per_hour | -0.4153124099300606 | -0.1608048398008565 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].inc_es | 0.8243248134764674 | 0.3384621004626619 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].inc_std | 0.28872924574902387 | 0.11028320679270323 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].inc_worst | -1.465292979659964 | -0.6912713575999824 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].max_abs_inventory | 3.2145 | 2.3391999999999995 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].max_drawdown | 15.420222394879795 | 6.656583119339859 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].net_bp_per_notional | -3.1020715226543047 | -3.2430075018506637 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].net_per_hour | -0.6245304661133347 | -0.2462445275601694 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].net_per_hour_over_inc_std | -2.068008367240835 | -2.0869123678885737 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].orders_per_fill | 26.02665802464394 | 32.604048465848805 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].own_edge_bp | 0.39807009598998766 | 0.5297143702882283 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].own_markout_1s_bp | -2.0937498666114633 | -1.8947869471968695 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].own_markout_30s_bp | -2.178621367422463 | -2.2967201131874333 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].own_markout_5s_bp | -2.162617730310149 | -2.256399302996632 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].paced_spells | 118.7 | 1.2 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].paced_time_share | 0.0002013839218764617 | 2.9325682848453213e-06 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].quote_presence_ask | 0.1422015116202487 | 0.13331137740710874 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].quote_presence_bid | 0.13510711240359363 | 0.15229153863017386 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].quote_presence_both | 7.115255604670243e-07 | 9.313392302250828e-07 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].turnover_per_hour | 1869.390680267487 | 766.5112893453847 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].tw_abs_inventory_avg | 0.7468031570164526 | 0.49396168075970637 |
| descriptive.scenarios[P4/conservative/tokyo/vip9].vol_closed_share | 0.037806092375100124 | 0.016701384486897154 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].fill_rate | 0.28981175256189673 | 0.27486157554575535 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].gate_active_share | 0.07744172312026938 | 0.0320452243615039 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].gross_bp_per_notional | -1.4418956227125495 | -1.389924572932948 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].gross_per_hour | -15.919445960915166 | -5.643822652431673 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].inc_es | 2.517789579411466 | 1.1844112411626475 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].inc_std | 0.7193145680867172 | 0.3656648338247877 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].inc_worst | -4.334646292760734 | -2.08165005711988 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].max_abs_inventory | 4.5017999999999825 | 4.623800000000001 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].max_drawdown | 161.69182169331336 | 57.928520501917944 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].net_bp_per_notional | -0.6428132975735172 | -0.591787032905944 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].net_per_hour | -7.319267635592302 | -2.3999183932452843 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].net_per_hour_over_inc_std | -8.67896800238284 | -6.095668817661366 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].orders_per_fill | 0.6775930490406155 | 0.9797147671482234 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].own_edge_bp | 0.27156368409572795 | 0.34664383384099534 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].own_markout_1s_bp | -1.1197145591599387 | -1.1264151789160146 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].own_markout_30s_bp | -1.428696290721171 | -1.3615305355410952 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].own_markout_5s_bp | -1.3198202607565332 | -1.3288618484544883 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].paced_spells | 3001.1 | 485.4 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].paced_time_share | 0.008624535616221327 | 0.0012944669499585638 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].quote_presence_ask | 0.8000851370201391 | 0.8430961532132321 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].quote_presence_bid | 0.8207016571681065 | 0.8448494697466356 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].quote_presence_both | 0.6689764433887283 | 0.7088603143981398 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].turnover_per_hour | 107633.10396573595 | 40627.47822281001 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].tw_abs_inventory_avg | 1.8323377051015188 | 1.9445713071080548 |
| descriptive.scenarios[P4/intermediate/distant/lp_tier4].vol_closed_share | 0.03160635056280029 | 0.015314377644294016 |
| descriptive.scenarios[P4/intermediate/distant/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P4/intermediate/distant/vip0].gate_active_share | 0.9620679298503891 | 0.983257015776277 |
| descriptive.scenarios[P4/intermediate/distant/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/intermediate/distant/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/intermediate/distant/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P4/intermediate/distant/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P4/intermediate/distant/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P4/intermediate/distant/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P4/intermediate/distant/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P4/intermediate/distant/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P4/intermediate/distant/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P4/intermediate/distant/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip0].vol_closed_share | 0.03793207014961088 | 0.016742984223722994 |
| descriptive.scenarios[P4/intermediate/distant/vip9].fill_rate | 0.015183700837587074 | 0.013487225641323342 |
| descriptive.scenarios[P4/intermediate/distant/vip9].gate_active_share | 0.9623947881472026 | 0.983344920604807 |
| descriptive.scenarios[P4/intermediate/distant/vip9].gross_bp_per_notional | -1.3118025316665594 | -1.7674647372093641 |
| descriptive.scenarios[P4/intermediate/distant/vip9].gross_per_hour | -0.6250824603720947 | -0.2533909371049564 |
| descriptive.scenarios[P4/intermediate/distant/vip9].inc_es | 0.8087433766854746 | 0.3711304322666757 |
| descriptive.scenarios[P4/intermediate/distant/vip9].inc_std | 0.27557847236971766 | 0.11497037918047001 |
| descriptive.scenarios[P4/intermediate/distant/vip9].inc_worst | -1.5515472587200416 | -0.863840043660065 |
| descriptive.scenarios[P4/intermediate/distant/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/distant/vip9].max_abs_inventory | 2.5028 | 2.1613999999999995 |
| descriptive.scenarios[P4/intermediate/distant/vip9].max_drawdown | 24.59841254219047 | 10.130220294960122 |
| descriptive.scenarios[P4/intermediate/distant/vip9].net_bp_per_notional | -2.4251460982036988 | -2.8799931299924983 |
| descriptive.scenarios[P4/intermediate/distant/vip9].net_per_hour | -1.0441273802025315 | -0.4013382408375167 |
| descriptive.scenarios[P4/intermediate/distant/vip9].net_per_hour_over_inc_std | -3.404455513916681 | -3.2917972770310513 |
| descriptive.scenarios[P4/intermediate/distant/vip9].orders_per_fill | 11.618223296370065 | 14.042619208832102 |
| descriptive.scenarios[P4/intermediate/distant/vip9].own_edge_bp | 0.28301572898057825 | 0.27031361377199964 |
| descriptive.scenarios[P4/intermediate/distant/vip9].own_markout_1s_bp | -1.703400437987468 | -1.680463678699887 |
| descriptive.scenarios[P4/intermediate/distant/vip9].own_markout_30s_bp | -1.7723850889989792 | -1.708298277206066 |
| descriptive.scenarios[P4/intermediate/distant/vip9].own_markout_5s_bp | -1.8515426038099654 | -1.7079183009073762 |
| descriptive.scenarios[P4/intermediate/distant/vip9].paced_spells | 93.2 | 0.8 |
| descriptive.scenarios[P4/intermediate/distant/vip9].paced_time_share | 0.00014673681408273038 | 1.634505427569788e-06 |
| descriptive.scenarios[P4/intermediate/distant/vip9].quote_presence_ask | 0.14201951919088174 | 0.13328881388842057 |
| descriptive.scenarios[P4/intermediate/distant/vip9].quote_presence_bid | 0.1271328588086066 | 0.1425929484614293 |
| descriptive.scenarios[P4/intermediate/distant/vip9].quote_presence_both | 5.918575271322891e-07 | 4.841366177067579e-07 |
| descriptive.scenarios[P4/intermediate/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P4/intermediate/distant/vip9].turnover_per_hour | 3777.343003080571 | 1331.6316190412545 |
| descriptive.scenarios[P4/intermediate/distant/vip9].tw_abs_inventory_avg | 0.656598188978291 | 0.44776232115249986 |
| descriptive.scenarios[P4/intermediate/distant/vip9].vol_closed_share | 0.037539417944860404 | 0.01665305202294285 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].fill_rate | 0.2865549355855794 | 0.26411010076340335 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].gate_active_share | 0.07829273029719341 | 0.03265474663801091 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].gross_bp_per_notional | -1.4750390831488311 | -1.4026524517659296 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].gross_per_hour | -18.84094320199744 | -6.282898871002938 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].inc_es | 2.593674406204086 | 1.2955884460373348 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].inc_std | 0.7183240098853123 | 0.38883911594191484 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].inc_worst | -3.922290483040361 | -2.254112819039638 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].max_abs_inventory | 4.54329999999994 | 4.7644 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].max_drawdown | 193.70848520387747 | 65.16350593699734 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].net_bp_per_notional | -0.675803383922431 | -0.6045877286788661 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].net_per_hour | -8.797548464674017 | -2.702366578123987 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].net_per_hour_over_inc_std | -10.54404482682275 | -6.45033186411068 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].orders_per_fill | 0.6240120153700417 | 0.9459919350155607 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].own_edge_bp | 0.24169230549996143 | 0.34821207835005746 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].own_markout_1s_bp | -1.1646612399873222 | -1.1510295460071345 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].own_markout_30s_bp | -1.4543553687347965 | -1.3878830779667772 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].own_markout_5s_bp | -1.3602286861543533 | -1.3522519434866886 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].paced_spells | 3551.3 | 573.4 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].paced_time_share | 0.009875463558894725 | 0.0015056467812875358 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].quote_presence_ask | 0.8229754268555688 | 0.8577268465552029 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].quote_presence_bid | 0.8403123118870713 | 0.862244415124897 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].quote_presence_both | 0.7080365458643181 | 0.7385005051552643 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].turnover_per_hour | 125659.62690916569 | 44833.618933246726 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].tw_abs_inventory_avg | 1.797524133460278 | 1.936898102806807 |
| descriptive.scenarios[P4/intermediate/regional/lp_tier4].vol_closed_share | 0.030953431316391538 | 0.015235222530026219 |
| descriptive.scenarios[P4/intermediate/regional/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P4/intermediate/regional/vip0].gate_active_share | 0.9620677937155758 | 0.9832570463064109 |
| descriptive.scenarios[P4/intermediate/regional/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/intermediate/regional/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/intermediate/regional/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P4/intermediate/regional/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P4/intermediate/regional/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P4/intermediate/regional/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P4/intermediate/regional/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P4/intermediate/regional/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P4/intermediate/regional/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P4/intermediate/regional/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip0].vol_closed_share | 0.03793220628442419 | 0.016742953693589243 |
| descriptive.scenarios[P4/intermediate/regional/vip9].fill_rate | 0.01078284469522919 | 0.010388513628316987 |
| descriptive.scenarios[P4/intermediate/regional/vip9].gate_active_share | 0.9621558214815515 | 0.9833092928634818 |
| descriptive.scenarios[P4/intermediate/regional/vip9].gross_bp_per_notional | -1.5716524936037795 | -1.931761565239451 |
| descriptive.scenarios[P4/intermediate/regional/vip9].gross_per_hour | -0.42458179220635983 | -0.20876897279156595 |
| descriptive.scenarios[P4/intermediate/regional/vip9].inc_es | 0.7841067435479011 | 0.31966255580933156 |
| descriptive.scenarios[P4/intermediate/regional/vip9].inc_std | 0.26900918511995625 | 0.10508983454372875 |
| descriptive.scenarios[P4/intermediate/regional/vip9].inc_worst | -1.4483421055100751 | -0.6043163638199822 |
| descriptive.scenarios[P4/intermediate/regional/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip9].max_abs_inventory | 2.6664000000000003 | 2.1092 |
| descriptive.scenarios[P4/intermediate/regional/vip9].max_drawdown | 17.06951809220019 | 8.097439175220003 |
| descriptive.scenarios[P4/intermediate/regional/vip9].net_bp_per_notional | -2.6860362728880682 | -3.0521894101123905 |
| descriptive.scenarios[P4/intermediate/regional/vip9].net_per_hour | -0.6916487497843283 | -0.32021125311902665 |
| descriptive.scenarios[P4/intermediate/regional/vip9].net_per_hour_over_inc_std | -2.5150531765801754 | -2.8848617081947756 |
| descriptive.scenarios[P4/intermediate/regional/vip9].orders_per_fill | 19.37636865576851 | 23.234782105508163 |
| descriptive.scenarios[P4/intermediate/regional/vip9].own_edge_bp | 0.2636395867245279 | 0.3364031006831732 |
| descriptive.scenarios[P4/intermediate/regional/vip9].own_markout_1s_bp | -1.9071303958839476 | -1.7635187457146124 |
| descriptive.scenarios[P4/intermediate/regional/vip9].own_markout_30s_bp | -1.852693979744938 | -1.720479835900576 |
| descriptive.scenarios[P4/intermediate/regional/vip9].own_markout_5s_bp | -2.0107814526154906 | -1.8685385027374206 |
| descriptive.scenarios[P4/intermediate/regional/vip9].paced_spells | 92.7 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip9].paced_time_share | 0.00014886191382044601 | 0.0 |
| descriptive.scenarios[P4/intermediate/regional/vip9].quote_presence_ask | 0.14375377221180446 | 0.13321794376491777 |
| descriptive.scenarios[P4/intermediate/regional/vip9].quote_presence_bid | 0.12997275354226345 | 0.1477944061944169 |
| descriptive.scenarios[P4/intermediate/regional/vip9].quote_presence_both | 7.010912756422831e-07 | 8.137472741390884e-07 |
| descriptive.scenarios[P4/intermediate/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P4/intermediate/regional/vip9].turnover_per_hour | 2399.2531801611904 | 998.4417477611954 |
| descriptive.scenarios[P4/intermediate/regional/vip9].tw_abs_inventory_avg | 0.6531215106908964 | 0.4686139975018199 |
| descriptive.scenarios[P4/intermediate/regional/vip9].vol_closed_share | 0.03774001291599951 | 0.016686316474401164 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].fill_rate | 0.2842254726023388 | 0.24402811388785892 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].gate_active_share | 0.08224257907528179 | 0.03380130531599172 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].gross_bp_per_notional | -1.6030128577407503 | -1.5234492438572613 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].gross_per_hour | -21.474017309786806 | -6.86133573180891 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].inc_es | 2.921726149815351 | 1.376259753909254 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].inc_std | 0.7767536045254821 | 0.40322237962136376 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].inc_worst | -4.2521995102413115 | -2.413395278719711 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].max_abs_inventory | 4.2270000000001176 | 4.091000000000004 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].max_drawdown | 237.16468466889538 | 78.41757797251725 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].net_bp_per_notional | -0.8037250737765408 | -0.7254320744467933 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].net_per_hour | -10.775973402281563 | -3.2592615818299135 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].net_per_hour_over_inc_std | -12.18884662369573 | -7.499155647647504 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].orders_per_fill | 0.6090956263754705 | 0.9899088238351913 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].own_edge_bp | 0.3652019116902065 | 0.5365064689848715 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].own_markout_1s_bp | -1.3072176030372566 | -1.2753801752941674 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].own_markout_30s_bp | -1.5937628118051035 | -1.5101047566609664 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].own_markout_5s_bp | -1.5007764622353006 | -1.4726234621212615 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].paced_spells | 3805.6 | 660.0 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].paced_time_share | 0.010523016438602024 | 0.0017389919627509409 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].quote_presence_ask | 0.8209526324855604 | 0.8641378344968915 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].quote_presence_bid | 0.8285402908985624 | 0.863433232035059 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].quote_presence_both | 0.6933723092789992 | 0.7455678637041905 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].turnover_per_hour | 133840.14285799867 | 45103.27410417107 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].tw_abs_inventory_avg | 1.87506541476996 | 1.9569564439505842 |
| descriptive.scenarios[P4/intermediate/tokyo/lp_tier4].vol_closed_share | 0.030863914634088375 | 0.01521459573538822 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].gate_active_share | 0.9620677704387482 | 0.9832570340571044 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip0].vol_closed_share | 0.037932229561251765 | 0.01674296594289569 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].fill_rate | 0.008976410850202229 | 0.008047691468216368 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].gate_active_share | 0.961821245032834 | 0.9832910655306575 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].gross_bp_per_notional | -2.0689394845988884 | -1.906863821790333 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].gross_per_hour | -0.43500171302754004 | -0.1578412110326558 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].inc_es | 0.8421537143567237 | 0.32724916102266405 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].inc_std | 0.2900819543848935 | 0.10707822513619607 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].inc_worst | -1.556936180839982 | -0.601715952979991 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].max_abs_inventory | 3.0752 | 2.2643999999999997 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].max_drawdown | 15.919530094149835 | 6.342305295939772 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].net_bp_per_notional | -3.1869897896059007 | -3.0283402850467596 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].net_per_hour | -0.6471010403419641 | -0.2461010594918327 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].net_per_hour_over_inc_std | -2.1221597119925653 | -2.1613952363753093 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].orders_per_fill | 27.071139984620885 | 34.48627208953285 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].own_edge_bp | 0.3967986191570726 | 0.545636422422646 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].own_markout_1s_bp | -2.0953251782907096 | -1.8142069361457835 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].own_markout_30s_bp | -2.1513496039772786 | -2.1884933311517782 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].own_markout_5s_bp | -2.1728370964375463 | -1.9834326550334052 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].paced_spells | 123.3 | 2.0 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].paced_time_share | 0.00020906643675682414 | 3.1773872437601717e-06 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].quote_presence_ask | 0.14311328639946239 | 0.13522643791809413 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].quote_presence_bid | 0.1329744486711249 | 0.1466169957317291 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].quote_presence_both | 5.875976988565013e-07 | 9.313392302250828e-07 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].turnover_per_hour | 1895.9889301656808 | 789.8265616077754 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].tw_abs_inventory_avg | 0.7198120017315255 | 0.478112030797152 |
| descriptive.scenarios[P4/intermediate/tokyo/vip9].vol_closed_share | 0.037808675153291525 | 0.016702178752223382 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].fill_rate | 0.41378577076003553 | 0.44472664408227286 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].gate_active_share | 0.0723063850304339 | 0.03181865292156363 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].gross_bp_per_notional | -1.0703489761083993 | -0.9690228863157712 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].gross_per_hour | -17.296875471085265 | -6.9516099166887475 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].inc_es | 2.293245488309059 | 1.0727530001280179 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].inc_std | 0.720514091396936 | 0.3651078282049006 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].inc_worst | -3.7593521451203826 | -1.7583418672000561 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].max_abs_inventory | 4.49359999999997 | 4.327599999999999 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].max_drawdown | 113.76943987984009 | 36.48890039155985 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].net_bp_per_notional | -0.2708673125723903 | -0.17014796705421265 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].net_per_hour | -5.062434819370327 | -1.397304562961008 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].net_per_hour_over_inc_std | -5.558591291000001 | -3.4220324290011552 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].orders_per_fill | 0.5909191219625185 | 0.7801011258228869 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].own_edge_bp | 0.4159447976226224 | 0.5801184865350095 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].own_markout_1s_bp | -0.7681417035129587 | -0.7242383798228872 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].own_markout_30s_bp | -1.0507024030694825 | -0.9479813802550531 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].own_markout_5s_bp | -0.9538211670853733 | -0.9201034915506321 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].paced_spells | 3982.0 | 855.6 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].paced_time_share | 0.011440286160980957 | 0.0023493094952489247 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].quote_presence_ask | 0.7577480295862304 | 0.814853779799642 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].quote_presence_bid | 0.7974213361476368 | 0.8125052087112801 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].quote_presence_both | 0.6094244456304334 | 0.6520808265085709 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].turnover_per_hour | 153050.01095336903 | 69504.98412746796 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].tw_abs_inventory_avg | 1.919000830883634 | 2.0051807584138177 |
| descriptive.scenarios[P4/optimistic/distant/lp_tier4].vol_closed_share | 0.031374128666959676 | 0.014634771478378637 |
| descriptive.scenarios[P4/optimistic/distant/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P4/optimistic/distant/vip0].gate_active_share | 0.9620679298503891 | 0.983257015776277 |
| descriptive.scenarios[P4/optimistic/distant/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/optimistic/distant/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/optimistic/distant/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P4/optimistic/distant/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P4/optimistic/distant/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P4/optimistic/distant/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P4/optimistic/distant/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P4/optimistic/distant/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P4/optimistic/distant/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P4/optimistic/distant/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip0].vol_closed_share | 0.03793207014961088 | 0.016742984223722994 |
| descriptive.scenarios[P4/optimistic/distant/vip9].fill_rate | 0.024999194990275104 | 0.027174335646095626 |
| descriptive.scenarios[P4/optimistic/distant/vip9].gate_active_share | 0.9622732821360931 | 0.9833518260236606 |
| descriptive.scenarios[P4/optimistic/distant/vip9].gross_bp_per_notional | -1.2001396873360595 | -1.4099754176561952 |
| descriptive.scenarios[P4/optimistic/distant/vip9].gross_per_hour | -0.9065873034739284 | -0.4098084100609657 |
| descriptive.scenarios[P4/optimistic/distant/vip9].inc_es | 0.9312693470176523 | 0.44485026174266507 |
| descriptive.scenarios[P4/optimistic/distant/vip9].inc_std | 0.29733872492353347 | 0.12727435780885005 |
| descriptive.scenarios[P4/optimistic/distant/vip9].inc_worst | -1.5981207992000486 | -0.839741420079992 |
| descriptive.scenarios[P4/optimistic/distant/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/distant/vip9].max_abs_inventory | 2.625999999999999 | 2.270600000000001 |
| descriptive.scenarios[P4/optimistic/distant/vip9].max_drawdown | 37.040382430990775 | 17.53537070227977 |
| descriptive.scenarios[P4/optimistic/distant/vip9].net_bp_per_notional | -2.307447970460635 | -2.514531176779559 |
| descriptive.scenarios[P4/optimistic/distant/vip9].net_per_hour | -1.5721075262008255 | -0.7203948715935241 |
| descriptive.scenarios[P4/optimistic/distant/vip9].net_per_hour_over_inc_std | -4.863036907020519 | -5.352602881650061 |
| descriptive.scenarios[P4/optimistic/distant/vip9].orders_per_fill | 10.882962522635015 | 14.635652936377516 |
| descriptive.scenarios[P4/optimistic/distant/vip9].own_edge_bp | 0.48257719721889225 | 0.6208693659061019 |
| descriptive.scenarios[P4/optimistic/distant/vip9].own_markout_1s_bp | -1.3365646457877143 | -1.2159597245016112 |
| descriptive.scenarios[P4/optimistic/distant/vip9].own_markout_30s_bp | -1.4423929824801331 | -1.2570994086621383 |
| descriptive.scenarios[P4/optimistic/distant/vip9].own_markout_5s_bp | -1.4444772561104569 | -1.2730751797255766 |
| descriptive.scenarios[P4/optimistic/distant/vip9].paced_spells | 85.3 | 1.2 |
| descriptive.scenarios[P4/optimistic/distant/vip9].paced_time_share | 0.00013796042830504753 | 1.8596779925823874e-06 |
| descriptive.scenarios[P4/optimistic/distant/vip9].quote_presence_ask | 0.1375230257041093 | 0.1394368557760587 |
| descriptive.scenarios[P4/optimistic/distant/vip9].quote_presence_bid | 0.13066171362338472 | 0.13599628048813 |
| descriptive.scenarios[P4/optimistic/distant/vip9].quote_presence_both | 4.793135521970742e-07 | 2.1288027200026236e-07 |
| descriptive.scenarios[P4/optimistic/distant/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P4/optimistic/distant/vip9].turnover_per_hour | 6025.824668493 | 2813.144730329089 |
| descriptive.scenarios[P4/optimistic/distant/vip9].tw_abs_inventory_avg | 0.6486532732415122 | 0.44827936355480835 |
| descriptive.scenarios[P4/optimistic/distant/vip9].vol_closed_share | 0.03758386459273274 | 0.01664671790033767 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].fill_rate | 0.4627042544948021 | 0.4940254113597365 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].gate_active_share | 0.08143042878435126 | 0.03632672984369957 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].gross_bp_per_notional | -1.1209180005464818 | -1.043521441009506 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].gross_per_hour | -23.721501386769017 | -9.568202690001389 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].inc_es | 2.5853425390302336 | 1.305102397642718 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].inc_std | 0.7575017514182725 | 0.41019437323657126 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].inc_worst | -4.173155461041118 | -2.1181248254403386 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].max_abs_inventory | 4.17010000000005 | 3.9974000000000087 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].max_drawdown | 167.85816281116655 | 60.33499998866313 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].net_bp_per_notional | -0.3213260555543357 | -0.2440580718494368 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].net_per_hour | -7.550897516238139 | -2.4150716299781485 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].net_per_hour_over_inc_std | -8.14645382020483 | -5.361009216161938 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].orders_per_fill | 0.5343639656837069 | 0.7107250194486407 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].own_edge_bp | 0.41184000297681733 | 0.5773607383504875 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].own_markout_1s_bp | -0.843372734715191 | -0.7998828535347557 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].own_markout_30s_bp | -1.1062425602305572 | -1.029970014085229 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].own_markout_5s_bp | -1.0274095421240972 | -0.9967972066831343 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].paced_spells | 5489.0 | 1195.4 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].paced_time_share | 0.014759035860104094 | 0.003184861520261847 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].quote_presence_ask | 0.7815470524890414 | 0.8262075435538396 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].quote_presence_bid | 0.8155317036319827 | 0.8285225938523734 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].quote_presence_both | 0.6466031573543946 | 0.6752923701539002 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].turnover_per_hour | 202241.87268215392 | 89468.13778097066 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].tw_abs_inventory_avg | 1.9016381627127612 | 2.0337922936118122 |
| descriptive.scenarios[P4/optimistic/regional/lp_tier4].vol_closed_share | 0.030265940896151745 | 0.014298221153506565 |
| descriptive.scenarios[P4/optimistic/regional/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P4/optimistic/regional/vip0].gate_active_share | 0.9620677937155758 | 0.9832570463064109 |
| descriptive.scenarios[P4/optimistic/regional/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/optimistic/regional/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/optimistic/regional/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P4/optimistic/regional/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P4/optimistic/regional/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P4/optimistic/regional/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P4/optimistic/regional/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P4/optimistic/regional/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P4/optimistic/regional/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P4/optimistic/regional/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip0].vol_closed_share | 0.03793220628442419 | 0.016742953693589243 |
| descriptive.scenarios[P4/optimistic/regional/vip9].fill_rate | 0.015606908594564328 | 0.01804111861757908 |
| descriptive.scenarios[P4/optimistic/regional/vip9].gate_active_share | 0.9620169385692344 | 0.9833132116588944 |
| descriptive.scenarios[P4/optimistic/regional/vip9].gross_bp_per_notional | -1.0981332220828377 | -1.3184020967031773 |
| descriptive.scenarios[P4/optimistic/regional/vip9].gross_per_hour | -0.4591968935953096 | -0.2567694138480452 |
| descriptive.scenarios[P4/optimistic/regional/vip9].inc_es | 0.769039216844881 | 0.3491634532640005 |
| descriptive.scenarios[P4/optimistic/regional/vip9].inc_std | 0.2637388895896695 | 0.10953107131622104 |
| descriptive.scenarios[P4/optimistic/regional/vip9].inc_worst | -1.4354811822299651 | -0.7917906199999883 |
| descriptive.scenarios[P4/optimistic/regional/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip9].max_abs_inventory | 2.8202 | 2.1616 |
| descriptive.scenarios[P4/optimistic/regional/vip9].max_drawdown | 20.27711575049018 | 11.223058086500092 |
| descriptive.scenarios[P4/optimistic/regional/vip9].net_bp_per_notional | -2.2051189994113516 | -2.428106552069678 |
| descriptive.scenarios[P4/optimistic/regional/vip9].net_per_hour | -0.8345751210703185 | -0.44893871854572714 |
| descriptive.scenarios[P4/optimistic/regional/vip9].net_per_hour_over_inc_std | -3.1232260421435183 | -3.878060107806239 |
| descriptive.scenarios[P4/optimistic/regional/vip9].orders_per_fill | 18.717297270273583 | 21.66311137603761 |
| descriptive.scenarios[P4/optimistic/regional/vip9].own_edge_bp | 0.4413364702942399 | 0.5956880983747826 |
| descriptive.scenarios[P4/optimistic/regional/vip9].own_markout_1s_bp | -1.5026619058369943 | -1.3262347998975752 |
| descriptive.scenarios[P4/optimistic/regional/vip9].own_markout_30s_bp | -1.5484704582725901 | -1.3131655925627328 |
| descriptive.scenarios[P4/optimistic/regional/vip9].own_markout_5s_bp | -1.584637366421763 | -1.327227908421527 |
| descriptive.scenarios[P4/optimistic/regional/vip9].paced_spells | 93.6 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip9].paced_time_share | 0.000149515971947329 | 0.0 |
| descriptive.scenarios[P4/optimistic/regional/vip9].quote_presence_ask | 0.13976979266886227 | 0.1354767835235935 |
| descriptive.scenarios[P4/optimistic/regional/vip9].quote_presence_bid | 0.13088604706484147 | 0.13635972308662675 |
| descriptive.scenarios[P4/optimistic/regional/vip9].quote_presence_both | 7.010912756422831e-07 | 8.198770385740151e-07 |
| descriptive.scenarios[P4/optimistic/regional/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P4/optimistic/regional/vip9].turnover_per_hour | 3387.5830530022495 | 1732.5775137420871 |
| descriptive.scenarios[P4/optimistic/regional/vip9].tw_abs_inventory_avg | 0.6188322701963893 | 0.41513423398955557 |
| descriptive.scenarios[P4/optimistic/regional/vip9].vol_closed_share | 0.03774029831262239 | 0.016681218644018784 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].fill_rate | 0.48781803915049726 | 0.5187242437123676 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].gate_active_share | 0.08609721812608198 | 0.039606228183131656 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].gross_bp_per_notional | -1.2626903639408427 | -1.1835132291501973 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].gross_per_hour | -29.82028967078068 | -12.48810552291996 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].inc_es | 3.118189714373128 | 1.625539908544188 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].inc_std | 0.8413855059651297 | 0.4705220712566078 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].inc_worst | -4.423905573920791 | -2.4646395859198655 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].max_abs_inventory | 4.000200000000112 | 3.9984000000000277 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].max_drawdown | 253.9463343602726 | 102.929391162067 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].net_bp_per_notional | -0.46303893300549437 | -0.3841641954237911 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].net_per_hour | -11.479433980996804 | -4.24298562311644 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].net_per_hour_over_inc_std | -11.754994271580458 | -8.214837229589623 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].orders_per_fill | 0.46467155326462883 | 0.6105421983822218 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].own_edge_bp | 0.4110723181817647 | 0.5769142861168592 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].own_markout_1s_bp | -0.9917287714467365 | -0.9416744241138642 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].own_markout_30s_bp | -1.250425889944911 | -1.1737176713306983 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].own_markout_5s_bp | -1.1742593821199316 | -1.1372419130706883 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].paced_spells | 4957.9 | 927.6 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].paced_time_share | 0.013072549516249882 | 0.0023987644372694844 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].quote_presence_ask | 0.7800138011521719 | 0.8233142502625406 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].quote_presence_bid | 0.8069095617522704 | 0.8261110220651059 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].quote_presence_both | 0.6333625769292666 | 0.6680372118861071 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].sessions | 10 | 5 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].turnover_per_hour | 229367.15593104978 | 103134.57379087104 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].tw_abs_inventory_avg | 2.0018454065170177 | 2.1086682269922243 |
| descriptive.scenarios[P4/optimistic/tokyo/lp_tier4].vol_closed_share | 0.02948237323722131 | 0.01409360261141164 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].fill_rate | None | undefined |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].gate_active_share | 0.9620677704387482 | 0.9832570340571044 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].gross_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].gross_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].inc_es | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].inc_std | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].inc_worst | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].max_abs_inventory | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].max_drawdown | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].net_bp_per_notional | None | undefined |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].net_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].net_per_hour_over_inc_std | None | undefined |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].orders_per_fill | None | undefined |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].own_edge_bp | None | undefined |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].own_markout_1s_bp | None | undefined |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].own_markout_30s_bp | None | undefined |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].own_markout_5s_bp | None | undefined |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].paced_spells | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].paced_time_share | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].quote_presence_ask | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].quote_presence_bid | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].quote_presence_both | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].sessions | 10 | 5 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].turnover_per_hour | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].tw_abs_inventory_avg | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip0].vol_closed_share | 0.037932229561251765 | 0.01674296594289569 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].fill_rate | 0.0142712056360127 | 0.01691355210800141 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].gate_active_share | 0.961704708006127 | 0.9832949342554042 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].gross_bp_per_notional | -1.259849085081455 | -1.5174896799356945 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].gross_per_hour | -0.44016199953110957 | -0.26952361350924725 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].inc_es | 0.795043332783486 | 0.37840196681999827 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].inc_std | 0.2789378471158404 | 0.11675713430041831 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].inc_worst | -1.3002307207799757 | -0.7633789072200015 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].liquidation_shortfall | 0.0 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].max_abs_inventory | 3.162200000000001 | 2.4712 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].max_drawdown | 18.697540468499447 | 11.120840155720042 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].net_bp_per_notional | -2.3724642346557867 | -2.627620118610035 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].net_per_hour | -0.7719880207457843 | -0.44965657291946715 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].net_per_hour_over_inc_std | -2.797725222863173 | -3.7032109578144463 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].orders_per_fill | 24.529331121049275 | 25.481712394025926 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].own_edge_bp | 0.42028679080125214 | 0.5846450182080758 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].own_markout_1s_bp | -1.606981106206473 | -1.338656720722805 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].own_markout_30s_bp | -1.5740818101983505 | -1.628731787277061 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].own_markout_5s_bp | -1.6574812632905025 | -1.443058619215408 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].paced_spells | 116.7 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].paced_time_share | 0.0001920594753483372 | 0.0 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].quote_presence_ask | 0.13795543119252912 | 0.13919480983891813 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].quote_presence_bid | 0.13438431055849281 | 0.13877651822744758 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].quote_presence_both | 8.040922816527345e-07 | 9.323137886945329e-07 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].sessions | 10 | 5 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].turnover_per_hour | 2982.620445474689 | 1624.3225844547821 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].tw_abs_inventory_avg | 0.6884630834807965 | 0.454445649823669 |
| descriptive.scenarios[P4/optimistic/tokyo/vip9].vol_closed_share | 0.03779258243907583 | 0.016693179127687204 |
| fee_split_per_hour_vip0.D_net_per_hour.gross_per_hour_mean |  | 4.168612668191124 |
| fee_split_per_hour_vip0.D_net_per_hour.maker_fees_per_hour_mean_mechanical |  | -29.73178178960304 |
| fee_split_per_hour_vip0.D_net_per_hour.taker_fees_per_hour_mean |  | 0.0032236450183797394 |
| fee_split_per_hour_vip0.P3_M2_minus_P0_net_per_hour.gross_per_hour_mean |  | 4.373098541420353 |
| fee_split_per_hour_vip0.P3_M2_minus_P0_net_per_hour.maker_fees_per_hour_mean_mechanical |  | -33.17783469087776 |
| fee_split_per_hour_vip0.P3_M2_minus_P0_net_per_hour.taker_fees_per_hour_mean |  | 0.010869973608513517 |

Not computed on test: e003_models.json (forwarded fit artifact, section 2).
Not computed on test: scenarios_by_period, forecasts_by_period (discovery split; every test session would be labelled train-late).

## E004

State: complete. Status: modeled historical replay under stress test.

H4-W is a statement about fill selection (E004 §6). Realised U vs P and net per hour are descriptive replications.

Tally (not independent replications): 2 of 2 confirmed.

| Check | Label | Discovery | Test | Status | Notes | Flag |
|---|---|---|---|---|---|---|
| H4-W[P0] | **confirmed (point estimate, 5 of 5 defined)** | -0.044 | D_W_bp: mean -0.08911; 5 defined, 2 +, 3 −; t-interval (descriptive, not used) ['-0.2864', '0.1081']; sessions 2026-06-01: 0.06464, 2026-07-01: -0.1344, 2026-08-01: -0.07852, 2026-09-01: 0.03584, 2026-10-01: -0.3331<br>D_W_stall_bp: mean -0.03572; 5 defined, 3 +, 2 −; t-interval (descriptive, not used) ['-0.2979', '0.2265']; sessions 2026-06-01: 0.06564, 2026-07-01: -0.1691, 2026-08-01: 0.1825, 2026-09-01: 0.07783, 2026-10-01: -0.3354 | modeled historical replay under stress test | mean D_W < 1 bp and D_W < 1 bp in at least 4 of 5 sessions (E004 §8; one-sided); no material deterioration under the specified threshold; A confirmed label means a replicated point estimate below the one-sided 1 bp threshold. It is not equivalence, not proof of no effect, and says nothing about deterioration smaller than 1 bp.; sign_count_below_delta: 5; sessions_D_W_negative: 3; mean_D_W_sign: negative; gates: {'overlap_share_mean': 0.0387160854968627, 'sessions_defined': 5, 'withdrawn_share_mean': 0.03830706107234673}; stall_only_result: rule holds; sensitive_to_natural_staleness: False; withdrawn_and_shares: {'wp_fill_share_install': 0.045868335028622344, 'wp_time_share_install': 0.04542388728572622, 'wu_fill_share_nostall': 0.08278568811275132, 'wu_time_share_nostall': 0.1905174666654788} |  |
| H4-W[P3_M2] | **confirmed (point estimate, 5 of 5 defined)** | -0.159 | D_W_bp: mean -0.08244; 5 defined, 2 +, 3 −; t-interval (descriptive, not used) ['-0.5331', '0.3682']; sessions 2026-06-01: 0.3591, 2026-07-01: -0.6409, 2026-08-01: -0.109, 2026-09-01: 0.05622, 2026-10-01: -0.07768<br>D_W_stall_bp: mean -0.02937; 5 defined, 2 +, 3 −; t-interval (descriptive, not used) ['-0.497', '0.4383']; sessions 2026-06-01: 0.3765, 2026-07-01: -0.6165, 2026-08-01: 0.2057, 2026-09-01: -0.03086, 2026-10-01: -0.08173 | modeled historical replay under stress test | mean D_W < 1 bp and D_W < 1 bp in at least 4 of 5 sessions (E004 §8; one-sided); no material deterioration under the specified threshold; A confirmed label means a replicated point estimate below the one-sided 1 bp threshold. It is not equivalence, not proof of no effect, and says nothing about deterioration smaller than 1 bp.; sign_count_below_delta: 5; sessions_D_W_negative: 3; mean_D_W_sign: negative; gates: {'overlap_share_mean': 0.0387160854968627, 'sessions_defined': 5, 'withdrawn_share_mean': 0.03830706107234673}; stall_only_result: rule holds; sensitive_to_natural_staleness: False; withdrawn_and_shares: {'wp_fill_share_install': 0.06657776531505506, 'wp_time_share_install': 0.04542388728572622, 'wu_fill_share_nostall': 0.0798639813657796, 'wu_time_share_nostall': 0.1905174666654788} |  |

H4-F y_view (secondary, shown separately): row label **confirmed (point estimate)**. Secondary. Largely implied by the target choice (E004 §0, §9); reported against the projection, not as a discovery.

- D1_S: **confirmed (point estimate, 5 of 5 defined)**. ρ_A 0.0107 (discovery -0.0067, not supported), projection 0.0, difference 0.0107; L 0.937 pp; A 0.0100 pp; leave-one-out ρ_A [0.004651738898762402, 0.019408834966030148]. Status: stress test. 
  A: 5 defined, 3 +, 2 −; t-interval (descriptive, not used) ['-0.01186', '0.03185'].
  L: 5 defined, 5 +, 0 −; t-interval (descriptive, not used) ['0.4063', '1.467'].
  Sessions: 2026-06-01: A 0.03265, L 0.9589, A/L 0.03405; 2026-07-01: A 0.0203, L 0.5479, A/L 0.03706; 2026-08-01: A -0.004457, L 0.5506, A/L -0.008094; 2026-09-01: A 0.01168, L 1.043, A/L 0.0112; 2026-10-01: A -0.0102, L 1.583, A/L -0.006442.
- D3: **confirmed (point estimate, 5 of 5 defined)**. ρ_A 0.0107 (discovery -0.0079, not supported), projection 0.0, difference 0.0107; L 0.934 pp; A 0.0099 pp; leave-one-out ρ_A [0.004382286357489094, 0.019439359134648188]. Status: stress test. 
  A: 5 defined, 3 +, 2 −; t-interval (descriptive, not used) ['-0.01294', '0.03284'].
  L: 5 defined, 5 +, 0 −; t-interval (descriptive, not used) ['0.4004', '1.467'].
  Sessions: 2026-06-01: A 0.03349, L 0.9624, A/L 0.0348; 2026-07-01: A 0.02099, L 0.5447, A/L 0.03853; 2026-08-01: A -0.00645, L 0.5395, A/L -0.01196; 2026-09-01: A 0.01201, L 1.042, A/L 0.01153; 2026-10-01: A -0.0103, L 1.581, A/L -0.006514.

| Item (reported only) | Discovery | Test |
|---|---|---|
| H4_0.difference_pp.defined | 10 | 5 |
| H4_0.difference_pp.mean | 0.030129009019508414 | 0.0014080074854215141 |
| H4_0.difference_pp.t_interval_95_descriptive_not_used |  | [-0.025993645602856604, 0.028809660573699634] |
| H4_0.discovery_label |  | harmless |
| H4_0.pending_review_flag |  | False |
| H4_0.status | observed (model trained under stress test) | observed (model trained under stress test) |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N.gross_bp.defined | 10 | 5 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N.gross_bp.mean | -0.001503486404884602 | 0.0053142570432380245 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N.gross_bp.positive | 4 | 3 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N.net_per_hour_vip0.defined | 10 | 5 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N.net_per_hour_vip0.mean | -1.1281217281139926 | -0.4439877797510306 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N.net_per_hour_vip0.positive | 0 | 0 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N.participation_ratios.notional | 1.0284085687246813 | 1.0167118706536311 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N.participation_ratios.presence | 1.040385301935996 | 1.0139358993471759 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N.pi5_bp.defined | 10 | 5 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N.pi5_bp.mean | 0.005421445525916812 | 0.0016278763596618174 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N.pi5_bp.positive | 8 | 4 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N[PL-lambda].gross_bp.defined | 10 | 5 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N[PL-lambda].gross_bp.mean | -0.044296115641659715 | -0.03868535855840312 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N[PL-lambda].gross_bp.positive | 3 | 1 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N[PL-lambda].net_per_hour_vip0.defined | 10 | 5 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N[PL-lambda].net_per_hour_vip0.mean | 3.247958782521858 | 3.5418326198852954 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N[PL-lambda].net_per_hour_vip0.positive | 10 | 5 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N[PL-lambda].participation_ratios.notional | 0.9210741570477159 | 0.8847151299834308 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N[PL-lambda].participation_ratios.presence | 0.9058309884381808 | 0.9454570542337116 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N[PL-lambda].pi5_bp.defined | 10 | 5 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N[PL-lambda].pi5_bp.mean | -0.035503844030981765 | -0.020235252776633718 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.N[UA-lambda] - N[PL-lambda].pi5_bp.positive | 2 | 1 |
| descriptive.p3_ua_vs_pl_forecasts_D1_S.status | modeled historical replay under stress test; participation-changing; descriptive | modeled historical replay under stress test; participation-changing; descriptive |
| descriptive.policy_D1_E.P0.P-N.delta_gross_bp.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.P-N.delta_gross_bp.mean | -0.04428910036039437 | -0.014058470699482494 |
| descriptive.policy_D1_E.P0.P-N.delta_gross_bp.positive | 1 | 1 |
| descriptive.policy_D1_E.P0.P-N.delta_net_per_hour_lp_tier4.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.P-N.delta_net_per_hour_lp_tier4.mean | 0.19497649121632837 | 0.037452496356265054 |
| descriptive.policy_D1_E.P0.P-N.delta_net_per_hour_lp_tier4.positive | 8 | 2 |
| descriptive.policy_D1_E.P0.P-N.delta_net_per_hour_vip0.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.P-N.delta_net_per_hour_vip0.mean | 8.026510873973988 | 4.696027769610611 |
| descriptive.policy_D1_E.P0.P-N.delta_net_per_hour_vip0.positive | 10 | 5 |
| descriptive.policy_D1_E.P0.P-N.delta_pi5_bp.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.P-N.delta_pi5_bp.mean | -0.05136001445039538 | -0.1190172152067587 |
| descriptive.policy_D1_E.P0.P-N.delta_pi5_bp.positive | 0 | 0 |
| descriptive.policy_D1_E.P0.P-N.fee_saving_per_hour_vip0_mechanical.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.P-N.fee_saving_per_hour_vip0_mechanical.mean | 7.247966184995439 | 4.317932831827234 |
| descriptive.policy_D1_E.P0.P-N.fee_saving_per_hour_vip0_mechanical.positive | 10 | 5 |
| descriptive.policy_D1_E.P0.P-N.participation_differs | False | False |
| descriptive.policy_D1_E.P0.P-N.participation_ratios.fills | 0.9622581938112746 | 0.9418125380062911 |
| descriptive.policy_D1_E.P0.P-N.participation_ratios.notional | 0.9308971543706775 | 0.8870053025955169 |
| descriptive.policy_D1_E.P0.P-N.participation_ratios.presence | 0.9682580462038729 | 0.9660089014353908 |
| descriptive.policy_D1_E.P0.U-N.delta_gross_bp.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-N.delta_gross_bp.mean | -0.056668051610596494 | -0.06403784801059449 |
| descriptive.policy_D1_E.P0.U-N.delta_gross_bp.positive | 1 | 1 |
| descriptive.policy_D1_E.P0.U-N.delta_net_per_hour_lp_tier4.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-N.delta_net_per_hour_lp_tier4.mean | 0.031904603929735285 | 0.02873785406791276 |
| descriptive.policy_D1_E.P0.U-N.delta_net_per_hour_lp_tier4.positive | 3 | 3 |
| descriptive.policy_D1_E.P0.U-N.delta_net_per_hour_vip0.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-N.delta_net_per_hour_vip0.mean | 6.813183699518406 | 4.188924661677352 |
| descriptive.policy_D1_E.P0.U-N.delta_net_per_hour_vip0.positive | 10 | 5 |
| descriptive.policy_D1_E.P0.U-N.delta_pi5_bp.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-N.delta_pi5_bp.mean | -0.051156478430132324 | -0.1141378438741166 |
| descriptive.policy_D1_E.P0.U-N.delta_pi5_bp.positive | 0 | 0 |
| descriptive.policy_D1_E.P0.U-N.fee_saving_per_hour_vip0_mechanical.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-N.fee_saving_per_hour_vip0_mechanical.mean | 6.277604450670802 | 3.85541157517455 |
| descriptive.policy_D1_E.P0.U-N.fee_saving_per_hour_vip0_mechanical.positive | 10 | 5 |
| descriptive.policy_D1_E.P0.U-N.participation_differs | False | False |
| descriptive.policy_D1_E.P0.U-N.participation_ratios.fills | 0.9668280434805782 | 0.952781032508007 |
| descriptive.policy_D1_E.P0.U-N.participation_ratios.notional | 0.936579686503406 | 0.9020446429483963 |
| descriptive.policy_D1_E.P0.U-N.participation_ratios.presence | 0.9696448457234812 | 0.9669197552563885 |
| descriptive.policy_D1_E.P0.U-P.avoided_loss_rate_usdt_per_hour.W_P.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-P.avoided_loss_rate_usdt_per_hour.W_P.mean | 0.6571671449870897 | 0.25293473869988187 |
| descriptive.policy_D1_E.P0.U-P.avoided_loss_rate_usdt_per_hour.W_P.positive | 10 | 5 |
| descriptive.policy_D1_E.P0.U-P.avoided_loss_rate_usdt_per_hour.W_U.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-P.avoided_loss_rate_usdt_per_hour.W_U.mean | 0.49917748753770325 | 0.20702999880206546 |
| descriptive.policy_D1_E.P0.U-P.avoided_loss_rate_usdt_per_hour.W_U.positive | 10 | 5 |
| descriptive.policy_D1_E.P0.U-P.delta_gross_bp.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-P.delta_gross_bp.mean | -0.012378951250202119 | -0.049979377311111996 |
| descriptive.policy_D1_E.P0.U-P.delta_gross_bp.positive | 3 | 3 |
| descriptive.policy_D1_E.P0.U-P.delta_gross_bp_over_s.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-P.delta_gross_bp_over_s.mean | -0.439608685012893 | -0.9872903837327097 |
| descriptive.policy_D1_E.P0.U-P.delta_gross_bp_over_s.positive | 3 | 3 |
| descriptive.policy_D1_E.P0.U-P.delta_net_per_hour_lp_tier4.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-P.delta_net_per_hour_lp_tier4.mean | -0.16307188728659308 | -0.008714642288352292 |
| descriptive.policy_D1_E.P0.U-P.delta_net_per_hour_lp_tier4.positive | 2 | 3 |
| descriptive.policy_D1_E.P0.U-P.delta_net_per_hour_vip0.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-P.delta_net_per_hour_vip0.mean | -1.2133271744555842 | -0.5071031079332581 |
| descriptive.policy_D1_E.P0.U-P.delta_net_per_hour_vip0.positive | 0 | 1 |
| descriptive.policy_D1_E.P0.U-P.delta_pi5_bp.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-P.delta_pi5_bp.mean | 0.00020353602026306205 | 0.0048793713326420905 |
| descriptive.policy_D1_E.P0.U-P.delta_pi5_bp.positive | 5 | 3 |
| descriptive.policy_D1_E.P0.U-P.fee_saving_per_hour_vip0_mechanical.defined | 10 | 5 |
| descriptive.policy_D1_E.P0.U-P.fee_saving_per_hour_vip0_mechanical.mean | -0.9703617343246395 | -0.46252125665268357 |
| descriptive.policy_D1_E.P0.U-P.fee_saving_per_hour_vip0_mechanical.positive | 0 | 0 |
| descriptive.policy_D1_E.P0.U-P.n_notional_share_in_wu | 0.023551975728443343 | 0.0313022823365976 |
| descriptive.policy_D1_E.P0.U-P.participation_differs | False | False |
| descriptive.policy_D1_E.P0.U-P.participation_ratios.fills | 1.0047171151332468 | 1.011914781273795 |
| descriptive.policy_D1_E.P0.U-P.participation_ratios.notional | 1.006130404554067 | 1.0193048676728302 |
| descriptive.policy_D1_E.P0.U-P.participation_ratios.presence | 1.0013685096419924 | 1.0008950452593133 |
| descriptive.policy_D1_E.P3_M2.P-N.delta_gross_bp.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.P-N.delta_gross_bp.mean | -0.034752460514922624 | -0.0915289768696852 |
| descriptive.policy_D1_E.P3_M2.P-N.delta_gross_bp.positive | 5 | 0 |
| descriptive.policy_D1_E.P3_M2.P-N.delta_net_per_hour_lp_tier4.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.P-N.delta_net_per_hour_lp_tier4.mean | 0.22162409894903118 | -0.025499616235099203 |
| descriptive.policy_D1_E.P3_M2.P-N.delta_net_per_hour_lp_tier4.positive | 8 | 2 |
| descriptive.policy_D1_E.P3_M2.P-N.delta_net_per_hour_vip0.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.P-N.delta_net_per_hour_vip0.mean | 1.732389384463577 | 1.9206373323953685 |
| descriptive.policy_D1_E.P3_M2.P-N.delta_net_per_hour_vip0.positive | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.P-N.delta_pi5_bp.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.P-N.delta_pi5_bp.mean | -0.053854044896730714 | -0.13040322262881152 |
| descriptive.policy_D1_E.P3_M2.P-N.delta_pi5_bp.positive | 1 | 0 |
| descriptive.policy_D1_E.P3_M2.P-N.fee_saving_per_hour_vip0_mechanical.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.P-N.fee_saving_per_hour_vip0_mechanical.mean | 1.3985699367377336 | 1.7932967222512406 |
| descriptive.policy_D1_E.P3_M2.P-N.fee_saving_per_hour_vip0_mechanical.positive | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.P-N.participation_differs | False | False |
| descriptive.policy_D1_E.P3_M2.P-N.participation_ratios.fills | 0.9798384585705063 | 0.9579602585738887 |
| descriptive.policy_D1_E.P3_M2.P-N.participation_ratios.notional | 0.9425735614976569 | 0.8899572034243433 |
| descriptive.policy_D1_E.P3_M2.P-N.participation_ratios.presence | 0.9799024472386172 | 0.9715642564572647 |
| descriptive.policy_D1_E.P3_M2.U-N.delta_gross_bp.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-N.delta_gross_bp.mean | -0.04963148682336125 | -0.12206969230600417 |
| descriptive.policy_D1_E.P3_M2.U-N.delta_gross_bp.positive | 4 | 1 |
| descriptive.policy_D1_E.P3_M2.U-N.delta_net_per_hour_lp_tier4.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-N.delta_net_per_hour_lp_tier4.mean | 0.20098614733244052 | -0.04012972937219715 |
| descriptive.policy_D1_E.P3_M2.U-N.delta_net_per_hour_lp_tier4.positive | 8 | 1 |
| descriptive.policy_D1_E.P3_M2.U-N.delta_net_per_hour_vip0.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-N.delta_net_per_hour_vip0.mean | 2.5095303321582043 | 2.2090479183093112 |
| descriptive.policy_D1_E.P3_M2.U-N.delta_net_per_hour_vip0.positive | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-N.delta_pi5_bp.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-N.delta_pi5_bp.mean | -0.06613150930580636 | -0.12306965021165142 |
| descriptive.policy_D1_E.P3_M2.U-N.delta_pi5_bp.positive | 0 | 0 |
| descriptive.policy_D1_E.P3_M2.U-N.fee_saving_per_hour_vip0_mechanical.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-N.fee_saving_per_hour_vip0_mechanical.mean | 2.1390515344983534 | 2.077247097147771 |
| descriptive.policy_D1_E.P3_M2.U-N.fee_saving_per_hour_vip0_mechanical.positive | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-N.participation_differs | False | False |
| descriptive.policy_D1_E.P3_M2.U-N.participation_ratios.fills | 0.9559332827189998 | 0.9434394797988828 |
| descriptive.policy_D1_E.P3_M2.U-N.participation_ratios.notional | 0.9245867510724372 | 0.8841959548982364 |
| descriptive.policy_D1_E.P3_M2.U-N.participation_ratios.presence | 0.9799805513052755 | 0.9671910740216957 |
| descriptive.policy_D1_E.P3_M2.U-P.avoided_loss_rate_usdt_per_hour.W_P.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-P.avoided_loss_rate_usdt_per_hour.W_P.mean | 0.18144524241147614 | 0.11805796541271182 |
| descriptive.policy_D1_E.P3_M2.U-P.avoided_loss_rate_usdt_per_hour.W_P.positive | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-P.avoided_loss_rate_usdt_per_hour.W_U.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-P.avoided_loss_rate_usdt_per_hour.W_U.mean | 0.2517904580562661 | 0.15222028490672282 |
| descriptive.policy_D1_E.P3_M2.U-P.avoided_loss_rate_usdt_per_hour.W_U.positive | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_gross_bp.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_gross_bp.mean | -0.014879026308438625 | -0.030540715436318977 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_gross_bp.positive | 4 | 1 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_gross_bp_over_s.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_gross_bp_over_s.mean | -0.3515610562492806 | -0.6232217258726863 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_gross_bp_over_s.positive | 4 | 1 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_net_per_hour_lp_tier4.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_net_per_hour_lp_tier4.mean | -0.020637951616590655 | -0.014630113137097944 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_net_per_hour_lp_tier4.positive | 4 | 1 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_net_per_hour_vip0.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_net_per_hour_vip0.mean | 0.7771409476946274 | 0.28841058591394264 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_net_per_hour_vip0.positive | 10 | 4 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_pi5_bp.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_pi5_bp.mean | -0.012277464409075645 | 0.007333572417160106 |
| descriptive.policy_D1_E.P3_M2.U-P.delta_pi5_bp.positive | 3 | 2 |
| descriptive.policy_D1_E.P3_M2.U-P.fee_saving_per_hour_vip0_mechanical.defined | 10 | 5 |
| descriptive.policy_D1_E.P3_M2.U-P.fee_saving_per_hour_vip0_mechanical.mean | 0.7404815977606198 | 0.28395037489653013 |
| descriptive.policy_D1_E.P3_M2.U-P.fee_saving_per_hour_vip0_mechanical.positive | 10 | 4 |
| descriptive.policy_D1_E.P3_M2.U-P.n_notional_share_in_wu | 0.04323170089199922 | 0.04661904916562829 |
| descriptive.policy_D1_E.P3_M2.U-P.participation_differs | False | False |
| descriptive.policy_D1_E.P3_M2.U-P.participation_ratios.fills | 0.9756411612873164 | 0.9852639782155416 |
| descriptive.policy_D1_E.P3_M2.U-P.participation_ratios.notional | 0.9812982601444382 | 0.9967481365072561 |
| descriptive.policy_D1_E.P3_M2.U-P.participation_ratios.presence | 1.000116186746492 | 0.9955106569886263 |
| descriptive.policy_D1_S.P0.P-N.delta_gross_bp.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.P-N.delta_gross_bp.mean | -0.07688220514057757 | -0.06311309978635186 |
| descriptive.policy_D1_S.P0.P-N.delta_gross_bp.positive | 1 | 1 |
| descriptive.policy_D1_S.P0.P-N.delta_net_per_hour_lp_tier4.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.P-N.delta_net_per_hour_lp_tier4.mean | 1.1701272748888234 | 0.3744020841806983 |
| descriptive.policy_D1_S.P0.P-N.delta_net_per_hour_lp_tier4.positive | 9 | 4 |
| descriptive.policy_D1_S.P0.P-N.delta_net_per_hour_vip0.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.P-N.delta_net_per_hour_vip0.mean | 26.057433478569482 | 11.327246588539046 |
| descriptive.policy_D1_S.P0.P-N.delta_net_per_hour_vip0.positive | 10 | 5 |
| descriptive.policy_D1_S.P0.P-N.delta_pi5_bp.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.P-N.delta_pi5_bp.mean | -0.06854597336600689 | -0.13571598601229687 |
| descriptive.policy_D1_S.P0.P-N.delta_pi5_bp.positive | 0 | 0 |
| descriptive.policy_D1_S.P0.P-N.fee_saving_per_hour_vip0_mechanical.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.P-N.fee_saving_per_hour_vip0_mechanical.mean | 23.03971193171532 | 10.142606602590645 |
| descriptive.policy_D1_S.P0.P-N.fee_saving_per_hour_vip0_mechanical.positive | 10 | 5 |
| descriptive.policy_D1_S.P0.P-N.participation_differs | True | True |
| descriptive.policy_D1_S.P0.P-N.participation_ratios.fills | 0.8662176153086673 | 0.8333491640622533 |
| descriptive.policy_D1_S.P0.P-N.participation_ratios.notional | 0.8300190437317514 | 0.7775513690568688 |
| descriptive.policy_D1_S.P0.P-N.participation_ratios.presence | 0.8646851251016789 | 0.855501468268568 |
| descriptive.policy_D1_S.P0.U-N.delta_gross_bp.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-N.delta_gross_bp.mean | -0.07038606174296355 | -0.07006447402728946 |
| descriptive.policy_D1_S.P0.U-N.delta_gross_bp.positive | 1 | 0 |
| descriptive.policy_D1_S.P0.U-N.delta_net_per_hour_lp_tier4.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-N.delta_net_per_hour_lp_tier4.mean | 0.528666498092366 | 0.237852394013842 |
| descriptive.policy_D1_S.P0.U-N.delta_net_per_hour_lp_tier4.positive | 9 | 4 |
| descriptive.policy_D1_S.P0.U-N.delta_net_per_hour_vip0.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-N.delta_net_per_hour_vip0.mean | 16.493757243268277 | 9.099154377534546 |
| descriptive.policy_D1_S.P0.U-N.delta_net_per_hour_vip0.positive | 10 | 5 |
| descriptive.policy_D1_S.P0.U-N.delta_pi5_bp.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-N.delta_pi5_bp.mean | -0.07521187020039152 | -0.12910651422637218 |
| descriptive.policy_D1_S.P0.U-N.delta_pi5_bp.positive | 0 | 0 |
| descriptive.policy_D1_S.P0.U-N.fee_saving_per_hour_vip0_mechanical.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-N.fee_saving_per_hour_vip0_mechanical.mean | 14.780233940982637 | 8.20746000101057 |
| descriptive.policy_D1_S.P0.U-N.fee_saving_per_hour_vip0_mechanical.positive | 10 | 5 |
| descriptive.policy_D1_S.P0.U-N.participation_differs | False | True |
| descriptive.policy_D1_S.P0.U-N.participation_ratios.fills | 0.9053073319776457 | 0.8634862868282902 |
| descriptive.policy_D1_S.P0.U-N.participation_ratios.notional | 0.8697263553632826 | 0.8157283501175229 |
| descriptive.policy_D1_S.P0.U-N.participation_ratios.presence | 0.9051095698526119 | 0.8854529469340797 |
| descriptive.policy_D1_S.P0.U-P.avoided_loss_rate_usdt_per_hour.W_P.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-P.avoided_loss_rate_usdt_per_hour.W_P.mean | 3.2317969597238196 | 1.0696956482975204 |
| descriptive.policy_D1_S.P0.U-P.avoided_loss_rate_usdt_per_hour.W_P.positive | 10 | 5 |
| descriptive.policy_D1_S.P0.U-P.avoided_loss_rate_usdt_per_hour.W_U.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-P.avoided_loss_rate_usdt_per_hour.W_U.mean | 1.5843859466935937 | 0.7766567463816522 |
| descriptive.policy_D1_S.P0.U-P.avoided_loss_rate_usdt_per_hour.W_U.positive | 10 | 5 |
| descriptive.policy_D1_S.P0.U-P.delta_gross_bp.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-P.delta_gross_bp.mean | 0.006496143397614018 | -0.006951374240937591 |
| descriptive.policy_D1_S.P0.U-P.delta_gross_bp.positive | 4 | 2 |
| descriptive.policy_D1_S.P0.U-P.delta_gross_bp_over_s.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-P.delta_gross_bp_over_s.mean | 0.01988369850863515 | -0.04928282856350604 |
| descriptive.policy_D1_S.P0.U-P.delta_gross_bp_over_s.positive | 4 | 2 |
| descriptive.policy_D1_S.P0.U-P.delta_net_per_hour_lp_tier4.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-P.delta_net_per_hour_lp_tier4.mean | -0.6414607767964574 | -0.13654969016685634 |
| descriptive.policy_D1_S.P0.U-P.delta_net_per_hour_lp_tier4.positive | 1 | 1 |
| descriptive.policy_D1_S.P0.U-P.delta_net_per_hour_vip0.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-P.delta_net_per_hour_vip0.mean | -9.563676235301207 | -2.2280922110045003 |
| descriptive.policy_D1_S.P0.U-P.delta_net_per_hour_vip0.positive | 1 | 0 |
| descriptive.policy_D1_S.P0.U-P.delta_pi5_bp.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-P.delta_pi5_bp.mean | -0.006665896834384633 | 0.006609471785924681 |
| descriptive.policy_D1_S.P0.U-P.delta_pi5_bp.positive | 4 | 3 |
| descriptive.policy_D1_S.P0.U-P.fee_saving_per_hour_vip0_mechanical.defined | 10 | 5 |
| descriptive.policy_D1_S.P0.U-P.fee_saving_per_hour_vip0_mechanical.mean | -8.259477990732682 | -1.9351466015800753 |
| descriptive.policy_D1_S.P0.U-P.fee_saving_per_hour_vip0_mechanical.positive | 1 | 0 |
| descriptive.policy_D1_S.P0.U-P.n_notional_share_in_wu | 0.08757643794786088 | 0.1181926779168804 |
| descriptive.policy_D1_S.P0.U-P.participation_differs | False | False |
| descriptive.policy_D1_S.P0.U-P.participation_ratios.fills | 1.044800009937113 | 1.036105929874778 |
| descriptive.policy_D1_S.P0.U-P.participation_ratios.notional | 1.04752994942697 | 1.0505907554971057 |
| descriptive.policy_D1_S.P0.U-P.participation_ratios.presence | 1.0466366622444532 | 1.034759911328027 |
| descriptive.policy_D1_S.P3_M2.P-N.delta_gross_bp.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.P-N.delta_gross_bp.mean | -0.023330116700626458 | -0.07321076483059026 |
| descriptive.policy_D1_S.P3_M2.P-N.delta_gross_bp.positive | 6 | 3 |
| descriptive.policy_D1_S.P3_M2.P-N.delta_net_per_hour_lp_tier4.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.P-N.delta_net_per_hour_lp_tier4.mean | 0.6975290709017445 | 0.17101146993406036 |
| descriptive.policy_D1_S.P3_M2.P-N.delta_net_per_hour_lp_tier4.positive | 9 | 4 |
| descriptive.policy_D1_S.P3_M2.P-N.delta_net_per_hour_vip0.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.P-N.delta_net_per_hour_vip0.mean | 6.381555395105101 | 4.995152584751045 |
| descriptive.policy_D1_S.P3_M2.P-N.delta_net_per_hour_vip0.positive | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.P-N.delta_pi5_bp.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.P-N.delta_pi5_bp.mean | -0.0671006224362087 | -0.14141778690046033 |
| descriptive.policy_D1_S.P3_M2.P-N.delta_pi5_bp.positive | 0 | 0 |
| descriptive.policy_D1_S.P3_M2.P-N.fee_saving_per_hour_vip0_mechanical.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.P-N.fee_saving_per_hour_vip0_mechanical.mean | 5.2603868358431916 | 4.462601859074472 |
| descriptive.policy_D1_S.P3_M2.P-N.fee_saving_per_hour_vip0_mechanical.positive | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.P-N.participation_differs | True | True |
| descriptive.policy_D1_S.P3_M2.P-N.participation_ratios.fills | 0.8816285681316801 | 0.8493227538939998 |
| descriptive.policy_D1_S.P3_M2.P-N.participation_ratios.notional | 0.8419770937341282 | 0.7808535735786826 |
| descriptive.policy_D1_S.P3_M2.P-N.participation_ratios.presence | 0.8798684810242516 | 0.8627247779851996 |
| descriptive.policy_D1_S.P3_M2.U-N.delta_gross_bp.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-N.delta_gross_bp.mean | 0.01809040963787607 | -0.1363236894055666 |
| descriptive.policy_D1_S.P3_M2.U-N.delta_gross_bp.positive | 6 | 1 |
| descriptive.policy_D1_S.P3_M2.U-N.delta_net_per_hour_lp_tier4.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-N.delta_net_per_hour_lp_tier4.mean | 0.7904497882706581 | 0.13368820025214628 |
| descriptive.policy_D1_S.P3_M2.U-N.delta_net_per_hour_lp_tier4.positive | 10 | 4 |
| descriptive.policy_D1_S.P3_M2.U-N.delta_net_per_hour_vip0.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-N.delta_net_per_hour_vip0.mean | 8.380713020122116 | 6.10531650370225 |
| descriptive.policy_D1_S.P3_M2.U-N.delta_net_per_hour_vip0.positive | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-N.delta_pi5_bp.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-N.delta_pi5_bp.mean | -0.12794013855317826 | -0.16200523310649487 |
| descriptive.policy_D1_S.P3_M2.U-N.delta_pi5_bp.positive | 0 | 0 |
| descriptive.policy_D1_S.P3_M2.U-N.fee_saving_per_hour_vip0_mechanical.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-N.fee_saving_per_hour_vip0_mechanical.mean | 7.037791695895066 | 5.525530233216417 |
| descriptive.policy_D1_S.P3_M2.U-N.fee_saving_per_hour_vip0_mechanical.positive | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-N.participation_differs | True | True |
| descriptive.policy_D1_S.P3_M2.U-N.participation_ratios.fills | 0.8141816401173003 | 0.7951347226945149 |
| descriptive.policy_D1_S.P3_M2.U-N.participation_ratios.notional | 0.7871373999113722 | 0.741886295590495 |
| descriptive.policy_D1_S.P3_M2.U-N.participation_ratios.presence | 0.9082339369265956 | 0.8748348975970647 |
| descriptive.policy_D1_S.P3_M2.U-P.avoided_loss_rate_usdt_per_hour.W_P.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-P.avoided_loss_rate_usdt_per_hour.W_P.mean | 0.9638222442434943 | 0.5356910557397326 |
| descriptive.policy_D1_S.P3_M2.U-P.avoided_loss_rate_usdt_per_hour.W_P.positive | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-P.avoided_loss_rate_usdt_per_hour.W_U.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-P.avoided_loss_rate_usdt_per_hour.W_U.mean | 0.8870491464727724 | 0.6093412643607307 |
| descriptive.policy_D1_S.P3_M2.U-P.avoided_loss_rate_usdt_per_hour.W_U.positive | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_gross_bp.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_gross_bp.mean | 0.04142052633850253 | -0.06311292457497635 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_gross_bp.positive | 5 | 2 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_gross_bp_over_s.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_gross_bp_over_s.mean | 0.11069572461145356 | -0.4159990570600092 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_gross_bp_over_s.positive | 5 | 2 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_net_per_hour_lp_tier4.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_net_per_hour_lp_tier4.mean | 0.09292071736891364 | -0.03732326968191404 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_net_per_hour_lp_tier4.positive | 8 | 2 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_net_per_hour_vip0.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_net_per_hour_vip0.mean | 1.999157625017014 | 1.1101639189512051 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_net_per_hour_vip0.positive | 9 | 4 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_pi5_bp.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_pi5_bp.mean | -0.06083951611696954 | -0.02058744620603452 |
| descriptive.policy_D1_S.P3_M2.U-P.delta_pi5_bp.positive | 0 | 1 |
| descriptive.policy_D1_S.P3_M2.U-P.fee_saving_per_hour_vip0_mechanical.defined | 10 | 5 |
| descriptive.policy_D1_S.P3_M2.U-P.fee_saving_per_hour_vip0_mechanical.mean | 1.7774048600518746 | 1.0629283741419442 |
| descriptive.policy_D1_S.P3_M2.U-P.fee_saving_per_hour_vip0_mechanical.positive | 9 | 4 |
| descriptive.policy_D1_S.P3_M2.U-P.n_notional_share_in_wu | 0.17314740313709956 | 0.18621077967250127 |
| descriptive.policy_D1_S.P3_M2.U-P.participation_differs | False | False |
| descriptive.policy_D1_S.P3_M2.U-P.participation_ratios.fills | 0.9229377455906016 | 0.9373929636506315 |
| descriptive.policy_D1_S.P3_M2.U-P.participation_ratios.notional | 0.9338379534275972 | 0.9544638603042713 |
| descriptive.policy_D1_S.P3_M2.U-P.participation_ratios.presence | 1.032612605094535 | 1.014028500516908 |
| descriptive.window_quality.D1_E:P0:conservative:regional.D_W_bp.defined | 10 | 5 |
| descriptive.window_quality.D1_E:P0:conservative:regional.D_W_bp.mean | -0.0820237288564986 | -0.21445110884117735 |
| descriptive.window_quality.D1_E:P0:conservative:regional.D_W_bp.positive | 2 | 2 |
| descriptive.window_quality.D1_E:P0:conservative:regional.replicates | 1 | 1 |
| descriptive.window_quality.D1_E:P0:conservative:regional.withdrawn_share_mean | 0.029464798214875694 | 0.03825177302163933 |
| descriptive.window_quality.D1_E:P0:intermediate:regional.D_W_bp.defined | 10 | 5 |
| descriptive.window_quality.D1_E:P0:intermediate:regional.D_W_bp.mean | -0.04357044098637425 | -0.08910642248306011 |
| descriptive.window_quality.D1_E:P0:intermediate:regional.D_W_bp.positive | 4 | 2 |
| descriptive.window_quality.D1_E:P0:intermediate:regional.replicates | 3 | 3 |
| descriptive.window_quality.D1_E:P0:intermediate:regional.withdrawn_share_mean | 0.029452842107774345 | 0.03830706107234673 |
| descriptive.window_quality.D1_E:P0:optimistic:regional.D_W_bp.defined | 10 | 5 |
| descriptive.window_quality.D1_E:P0:optimistic:regional.D_W_bp.mean | -0.10068942237316345 | -0.41263933559546295 |
| descriptive.window_quality.D1_E:P0:optimistic:regional.D_W_bp.positive | 2 | 0 |
| descriptive.window_quality.D1_E:P0:optimistic:regional.replicates | 1 | 1 |
| descriptive.window_quality.D1_E:P0:optimistic:regional.withdrawn_share_mean | 0.029464798214875694 | 0.03825177302163933 |
| descriptive.window_quality.D1_E:P3_M2:conservative:regional.D_W_bp.defined | 10 | 5 |
| descriptive.window_quality.D1_E:P3_M2:conservative:regional.D_W_bp.mean | -0.40818430112294146 | -0.35437192891877334 |
| descriptive.window_quality.D1_E:P3_M2:conservative:regional.D_W_bp.positive | 3 | 2 |
| descriptive.window_quality.D1_E:P3_M2:conservative:regional.replicates | 1 | 1 |
| descriptive.window_quality.D1_E:P3_M2:conservative:regional.withdrawn_share_mean | 0.029464798214875694 | 0.03825177302163933 |
| descriptive.window_quality.D1_E:P3_M2:intermediate:regional.D_W_bp.defined | 10 | 5 |
| descriptive.window_quality.D1_E:P3_M2:intermediate:regional.D_W_bp.mean | -0.15914111915455992 | -0.08244476568187102 |
| descriptive.window_quality.D1_E:P3_M2:intermediate:regional.D_W_bp.positive | 2 | 2 |
| descriptive.window_quality.D1_E:P3_M2:intermediate:regional.replicates | 3 | 3 |
| descriptive.window_quality.D1_E:P3_M2:intermediate:regional.withdrawn_share_mean | 0.029452842107774345 | 0.03830706107234673 |
| descriptive.window_quality.D1_E:P3_M2:optimistic:regional.D_W_bp.defined | 10 | 5 |
| descriptive.window_quality.D1_E:P3_M2:optimistic:regional.D_W_bp.mean | -0.3102813439028407 | -0.2965671784114009 |
| descriptive.window_quality.D1_E:P3_M2:optimistic:regional.D_W_bp.positive | 2 | 1 |
| descriptive.window_quality.D1_E:P3_M2:optimistic:regional.replicates | 1 | 1 |
| descriptive.window_quality.D1_E:P3_M2:optimistic:regional.withdrawn_share_mean | 0.029464798214875694 | 0.03825177302163933 |
| descriptive.window_quality.D1_S:P0:intermediate:regional.D_W_bp.defined | 10 | 5 |
| descriptive.window_quality.D1_S:P0:intermediate:regional.D_W_bp.mean | -0.13832085738537803 | -0.11803658935515027 |
| descriptive.window_quality.D1_S:P0:intermediate:regional.D_W_bp.positive | 0 | 1 |
| descriptive.window_quality.D1_S:P0:intermediate:regional.replicates | 3 | 3 |
| descriptive.window_quality.D1_S:P0:intermediate:regional.withdrawn_share_mean | 0.13998004662420854 | 0.14854523902174002 |
| descriptive.window_quality.D1_S:P3_M2:intermediate:regional.D_W_bp.defined | 10 | 5 |
| descriptive.window_quality.D1_S:P3_M2:intermediate:regional.D_W_bp.mean | -0.3160920612219398 | -0.1890192740061151 |
| descriptive.window_quality.D1_S:P3_M2:intermediate:regional.D_W_bp.positive | 0 | 0 |
| descriptive.window_quality.D1_S:P3_M2:intermediate:regional.replicates | 3 | 3 |
| descriptive.window_quality.D1_S:P3_M2:intermediate:regional.withdrawn_share_mean | 0.13998004662420854 | 0.14854523902174002 |
| h4f_other.D1_E:y_k.A.defined | 10 | 5 |
| h4f_other.D1_E:y_k.A.mean | 0.07200489364070348 | 0.02240247170074392 |
| h4f_other.D1_E:y_k.A.negative |  | 0 |
| h4f_other.D1_E:y_k.A.positive | 10 | 5 |
| h4f_other.D1_E:y_k.A.t_interval_95_descriptive_not_used |  | [-0.020087665111288705, 0.06489260851277655] |
| h4f_other.D1_E:y_k.B.defined | 10 | 5 |
| h4f_other.D1_E:y_k.B.mean | 0.0046207641398808615 | 0.015462207637040227 |
| h4f_other.D1_E:y_k.B.negative |  | 1 |
| h4f_other.D1_E:y_k.B.positive | 7 | 4 |
| h4f_other.D1_E:y_k.B.t_interval_95_descriptive_not_used |  | [-0.012981010041655158, 0.04390542531573561] |
| h4f_other.D1_E:y_k.C.defined | 10 | 5 |
| h4f_other.D1_E:y_k.C.mean | 0.06726869907673341 | 0.006903503823916068 |
| h4f_other.D1_E:y_k.C.negative |  | 4 |
| h4f_other.D1_E:y_k.C.positive | 6 | 1 |
| h4f_other.D1_E:y_k.C.t_interval_95_descriptive_not_used |  | [-0.06314489415496771, 0.07695190180279984] |
| h4f_other.D1_E:y_k.L.defined | 10 | 5 |
| h4f_other.D1_E:y_k.L.mean | 0.16397455480718137 | 0.13853536073183506 |
| h4f_other.D1_E:y_k.L.negative |  | 0 |
| h4f_other.D1_E:y_k.L.positive | 10 | 5 |
| h4f_other.D1_E:y_k.L.t_interval_95_descriptive_not_used |  | [0.10542528408916937, 0.17164543737450075] |
| h4f_other.D1_E:y_k.cell |  | D1_E |
| h4f_other.D1_E:y_k.components_defined_ok |  | True |
| h4f_other.D1_E:y_k.gate_passes |  | False |
| h4f_other.D1_E:y_k.leave_one_out_rho_A_range |  | [0.04845829549390132, 0.19891403656854983] |
| h4f_other.D1_E:y_k.per_session.2026-06-01.A |  | 0.005153029402448439 |
| h4f_other.D1_E:y_k.per_session.2026-06-01.A_over_L |  | 0.03415202914030497 |
| h4f_other.D1_E:y_k.per_session.2026-06-01.L |  | 0.15088501421917044 |
| h4f_other.D1_E:y_k.per_session.2026-07-01.A |  | 0.01118635496484277 |
| h4f_other.D1_E:y_k.per_session.2026-07-01.A_over_L |  | 0.09059164221712801 |
| h4f_other.D1_E:y_k.per_session.2026-07-01.L |  | 0.12348109263801144 |
| h4f_other.D1_E:y_k.per_session.2026-08-01.A |  | 0.08340191631596161 |
| h4f_other.D1_E:y_k.per_session.2026-08-01.A_over_L |  | 0.8155622532766816 |
| h4f_other.D1_E:y_k.per_session.2026-08-01.L |  | 0.10226309025568314 |
| h4f_other.D1_E:y_k.per_session.2026-09-01.A |  | 0.003831509518569476 |
| h4f_other.D1_E:y_k.per_session.2026-09-01.A_over_L |  | 0.026596233055337364 |
| h4f_other.D1_E:y_k.per_session.2026-09-01.L |  | 0.1440621125028292 |
| h4f_other.D1_E:y_k.per_session.2026-10-01.A |  | 0.008439548301897304 |
| h4f_other.D1_E:y_k.per_session.2026-10-01.A_over_L |  | 0.04907127981249181 |
| h4f_other.D1_E:y_k.per_session.2026-10-01.L |  | 0.17198549404348107 |
| h4f_other.D1_E:y_k.rho_A |  | 0.1617094118238066 |
| h4f_other.D1_E:y_k.rho_B |  | 0.11161199245707852 |
| h4f_other.D1_E:y_k.status | stress test | stress test |
| h4f_other.D1_E:y_k.sum_L |  | 0.6926768036591753 |
| h4f_other.D1_E:y_k.target |  | y_k |
| h4f_other.D1_E:y_view.A.defined | 10 | 5 |
| h4f_other.D1_E:y_view.A.mean | -0.0066772857828512056 | -0.000377431069737888 |
| h4f_other.D1_E:y_view.A.negative |  | 1 |
| h4f_other.D1_E:y_view.A.positive | 5 | 4 |
| h4f_other.D1_E:y_view.A.t_interval_95_descriptive_not_used |  | [-0.012193089677219658, 0.011438227537743881] |
| h4f_other.D1_E:y_view.B.defined | 10 | 5 |
| h4f_other.D1_E:y_view.B.mean | 0.0002054569433351805 | 0.0005373405690335175 |
| h4f_other.D1_E:y_view.B.negative |  | 1 |
| h4f_other.D1_E:y_view.B.positive | 5 | 4 |
| h4f_other.D1_E:y_view.B.t_interval_95_descriptive_not_used |  | [-6.776308114185938e-05, 0.0011424442192088944] |
| h4f_other.D1_E:y_view.C.defined | 10 | 5 |
| h4f_other.D1_E:y_view.C.mean | -0.0069955390162011796 | -0.0009464208599727186 |
| h4f_other.D1_E:y_view.C.negative |  | 1 |
| h4f_other.D1_E:y_view.C.positive | 5 | 4 |
| h4f_other.D1_E:y_view.C.t_interval_95_descriptive_not_used |  | [-0.013030824080888017, 0.01113798236094258] |
| h4f_other.D1_E:y_view.L.defined | 10 | 5 |
| h4f_other.D1_E:y_view.L.mean | 0.1632057986399583 | 0.1705306851962507 |
| h4f_other.D1_E:y_view.L.negative |  | 0 |
| h4f_other.D1_E:y_view.L.positive | 10 | 5 |
| h4f_other.D1_E:y_view.L.t_interval_95_descriptive_not_used |  | [0.10942295180551875, 0.23163841858698264] |
| h4f_other.D1_E:y_view.cell |  | D1_E |
| h4f_other.D1_E:y_view.components_defined_ok |  | True |
| h4f_other.D1_E:y_view.gate_passes |  | False |
| h4f_other.D1_E:y_view.leave_one_out_rho_A_range |  | [-0.010109073785581133, 0.021118141558978093] |
| h4f_other.D1_E:y_view.per_session.2026-06-01.A |  | 0.0051230061262952376 |
| h4f_other.D1_E:y_view.per_session.2026-06-01.A_over_L |  | 0.032179479270842866 |
| h4f_other.D1_E:y_view.per_session.2026-06-01.L |  | 0.15920102631794553 |
| h4f_other.D1_E:y_view.per_session.2026-07-01.A |  | 0.0036927711247303208 |
| h4f_other.D1_E:y_view.per_session.2026-07-01.A_over_L |  | 0.02734305133123652 |
| h4f_other.D1_E:y_view.per_session.2026-07-01.L |  | 0.1350533662097808 |
| h4f_other.D1_E:y_view.per_session.2026-08-01.A |  | -0.017332336631348255 |
| h4f_other.D1_E:y_view.per_session.2026-08-01.A_over_L |  | -0.14290804953054145 |
| h4f_other.D1_E:y_view.per_session.2026-08-01.L |  | 0.12128313757192588 |
| h4f_other.D1_E:y_view.per_session.2026-09-01.A |  | 0.0038901026406694683 |
| h4f_other.D1_E:y_view.per_session.2026-09-01.A_over_L |  | 0.020110997470364038 |
| h4f_other.D1_E:y_view.per_session.2026-09-01.L |  | 0.19343161105768125 |
| h4f_other.D1_E:y_view.per_session.2026-10-01.A |  | 0.0027393013909637887 |
| h4f_other.D1_E:y_view.per_session.2026-10-01.A_over_L |  | 0.011241190185666414 |
| h4f_other.D1_E:y_view.per_session.2026-10-01.L |  | 0.24368428482392002 |
| h4f_other.D1_E:y_view.rho_A |  | -0.0022132736363753625 |
| h4f_other.D1_E:y_view.rho_B |  | 0.0031509905001269036 |
| h4f_other.D1_E:y_view.status | stress test | stress test |
| h4f_other.D1_E:y_view.sum_L |  | 0.8526534259812535 |
| h4f_other.D1_E:y_view.target |  | y_view |
| h4f_other.D1_S1:y_k.A.defined | 10 | 5 |
| h4f_other.D1_S1:y_k.A.mean | 0.03357051309451853 | 0.013179012217050446 |
| h4f_other.D1_S1:y_k.A.negative |  | 0 |
| h4f_other.D1_S1:y_k.A.positive | 9 | 5 |
| h4f_other.D1_S1:y_k.A.t_interval_95_descriptive_not_used |  | [-0.00023999559589394856, 0.02659802002999484] |
| h4f_other.D1_S1:y_k.B.defined | 10 | 5 |
| h4f_other.D1_S1:y_k.B.mean | 0.009147985822112048 | 0.010821800613800382 |
| h4f_other.D1_S1:y_k.B.negative |  | 1 |
| h4f_other.D1_S1:y_k.B.positive | 9 | 4 |
| h4f_other.D1_S1:y_k.B.t_interval_95_descriptive_not_used |  | [-0.007390018836732078, 0.02903362006433284] |
| h4f_other.D1_S1:y_k.C.defined | 10 | 5 |
| h4f_other.D1_S1:y_k.C.mean | 0.024488917568030732 | 0.002515587083666748 |
| h4f_other.D1_S1:y_k.C.negative |  | 4 |
| h4f_other.D1_S1:y_k.C.positive | 6 | 1 |
| h4f_other.D1_S1:y_k.C.t_interval_95_descriptive_not_used |  | [-0.025053510042034977, 0.03008468420936847] |
| h4f_other.D1_S1:y_k.L.defined | 10 | 5 |
| h4f_other.D1_S1:y_k.L.mean | 0.06428383257692247 | 0.06480009072354927 |
| h4f_other.D1_S1:y_k.L.negative |  | 0 |
| h4f_other.D1_S1:y_k.L.positive | 10 | 5 |
| h4f_other.D1_S1:y_k.L.t_interval_95_descriptive_not_used |  | [0.03889411978206285, 0.09070606166503568] |
| h4f_other.D1_S1:y_k.cell |  | D1_S1 |
| h4f_other.D1_S1:y_k.components_defined_ok |  | True |
| h4f_other.D1_S1:y_k.gate_passes |  | False |
| h4f_other.D1_S1:y_k.leave_one_out_rho_A_range |  | [0.13332887940753435, 0.24349453128215098] |
| h4f_other.D1_S1:y_k.per_session.2026-06-01.A |  | 0.009229416433297999 |
| h4f_other.D1_S1:y_k.per_session.2026-06-01.A_over_L |  | 0.11870235040332 |
| h4f_other.D1_S1:y_k.per_session.2026-06-01.L |  | 0.07775260053350941 |
| h4f_other.D1_S1:y_k.per_session.2026-07-01.A |  | 0.006494462264161616 |
| h4f_other.D1_S1:y_k.per_session.2026-07-01.A_over_L |  | 0.14395896177302672 |
| h4f_other.D1_S1:y_k.per_session.2026-07-01.L |  | 0.04511328912194523 |
| h4f_other.D1_S1:y_k.per_session.2026-08-01.A |  | 0.028825585021974298 |
| h4f_other.D1_S1:y_k.per_session.2026-08-01.A_over_L |  | 0.6270507943683413 |
| h4f_other.D1_S1:y_k.per_session.2026-08-01.L |  | 0.04597009569378141 |
| h4f_other.D1_S1:y_k.per_session.2026-09-01.A |  | 0.0020261505100931387 |
| h4f_other.D1_S1:y_k.per_session.2026-09-01.A_over_L |  | 0.03283914751762232 |
| h4f_other.D1_S1:y_k.per_session.2026-09-01.L |  | 0.061699242010038624 |
| h4f_other.D1_S1:y_k.per_session.2026-10-01.A |  | 0.019319446855725175 |
| h4f_other.D1_S1:y_k.per_session.2026-10-01.A_over_L |  | 0.2067019749387711 |
| h4f_other.D1_S1:y_k.per_session.2026-10-01.L |  | 0.09346522625847165 |
| h4f_other.D1_S1:y_k.rho_A |  | 0.20337953342187232 |
| h4f_other.D1_S1:y_k.rho_B |  | 0.16700286207882709 |
| h4f_other.D1_S1:y_k.status | stress test | stress test |
| h4f_other.D1_S1:y_k.sum_L |  | 0.3240004536177463 |
| h4f_other.D1_S1:y_k.target |  | y_k |
| h4f_other.D1_S1:y_view.A.defined | 10 | 5 |
| h4f_other.D1_S1:y_view.A.mean | -0.0031123934132093467 | -0.0007163252359832839 |
| h4f_other.D1_S1:y_view.A.negative |  | 3 |
| h4f_other.D1_S1:y_view.A.positive | 2 | 2 |
| h4f_other.D1_S1:y_view.A.t_interval_95_descriptive_not_used |  | [-0.003805757517796009, 0.002373107045829441] |
| h4f_other.D1_S1:y_view.B.defined | 10 | 5 |
| h4f_other.D1_S1:y_view.B.mean | 4.280273690033809e-05 | -0.0002630021229754753 |
| h4f_other.D1_S1:y_view.B.negative |  | 3 |
| h4f_other.D1_S1:y_view.B.positive | 4 | 2 |
| h4f_other.D1_S1:y_view.B.t_interval_95_descriptive_not_used |  | [-0.002221120985921189, 0.0016951167399702383] |
| h4f_other.D1_S1:y_view.C.defined | 10 | 5 |
| h4f_other.D1_S1:y_view.C.mean | -0.0030611331065943936 | -0.0002680055949434212 |
| h4f_other.D1_S1:y_view.C.negative |  | 1 |
| h4f_other.D1_S1:y_view.C.positive | 5 | 4 |
| h4f_other.D1_S1:y_view.C.t_interval_95_descriptive_not_used |  | [-0.0034692746299480304, 0.0029332634400611878] |
| h4f_other.D1_S1:y_view.L.defined | 10 | 5 |
| h4f_other.D1_S1:y_view.L.mean | 0.06691241522325156 | 0.07947599350596404 |
| h4f_other.D1_S1:y_view.L.negative |  | 0 |
| h4f_other.D1_S1:y_view.L.positive | 10 | 5 |
| h4f_other.D1_S1:y_view.L.t_interval_95_descriptive_not_used |  | [0.04603179693306757, 0.11292019007886052] |
| h4f_other.D1_S1:y_view.cell |  | D1_S1 |
| h4f_other.D1_S1:y_view.components_defined_ok |  | True |
| h4f_other.D1_S1:y_view.gate_passes |  | False |
| h4f_other.D1_S1:y_view.leave_one_out_rho_A_range |  | [-0.018648229150852937, 0.001212087736024394] |
| h4f_other.D1_S1:y_view.per_session.2026-06-01.A |  | -0.0008544757586275153 |
| h4f_other.D1_S1:y_view.per_session.2026-06-01.A_over_L |  | -0.009162146451721885 |
| h4f_other.D1_S1:y_view.per_session.2026-06-01.L |  | 0.09326152590225512 |
| h4f_other.D1_S1:y_view.per_session.2026-07-01.A |  | 0.0008351607493684021 |
| h4f_other.D1_S1:y_view.per_session.2026-07-01.A_over_L |  | 0.018994366850497147 |
| h4f_other.D1_S1:y_view.per_session.2026-07-01.L |  | 0.04396886487145757 |
| h4f_other.D1_S1:y_view.per_session.2026-08-01.A |  | -0.003978631360623819 |
| h4f_other.D1_S1:y_view.per_session.2026-08-01.A_over_L |  | -0.05696645911626472 |
| h4f_other.D1_S1:y_view.per_session.2026-08-01.L |  | 0.06984164756499434 |
| h4f_other.D1_S1:y_view.per_session.2026-09-01.A |  | 0.0024425677900730136 |
| h4f_other.D1_S1:y_view.per_session.2026-09-01.A_over_L |  | 0.032858383669341074 |
| h4f_other.D1_S1:y_view.per_session.2026-09-01.L |  | 0.07433621247633315 |
| h4f_other.D1_S1:y_view.per_session.2026-10-01.A |  | -0.002026247600106501 |
| h4f_other.D1_S1:y_view.per_session.2026-10-01.A_over_L |  | -0.01747191175146471 |
| h4f_other.D1_S1:y_view.per_session.2026-10-01.L |  | 0.11597171671478002 |
| h4f_other.D1_S1:y_view.rho_A |  | -0.00901310199953058 |
| h4f_other.D1_S1:y_view.rho_B |  | -0.003309202079439738 |
| h4f_other.D1_S1:y_view.status | stress test | stress test |
| h4f_other.D1_S1:y_view.sum_L |  | 0.3973799675298202 |
| h4f_other.D1_S1:y_view.target |  | y_view |
| h4f_other.D1_S3:y_k.A.defined | 10 | 5 |
| h4f_other.D1_S3:y_k.A.mean | 1.574415539743356 | 0.9667611499968022 |
| h4f_other.D1_S3:y_k.A.negative |  | 0 |
| h4f_other.D1_S3:y_k.A.positive | 10 | 5 |
| h4f_other.D1_S3:y_k.A.t_interval_95_descriptive_not_used |  | [0.4790804940791227, 1.4544418059144817] |
| h4f_other.D1_S3:y_k.B.defined | 10 | 5 |
| h4f_other.D1_S3:y_k.B.mean | 0.36183755101028336 | 0.5770445991729356 |
| h4f_other.D1_S3:y_k.B.negative |  | 1 |
| h4f_other.D1_S3:y_k.B.positive | 8 | 4 |
| h4f_other.D1_S3:y_k.B.t_interval_95_descriptive_not_used |  | [0.07303258109896904, 1.0810566172469023] |
| h4f_other.D1_S3:y_k.C.defined | 10 | 5 |
| h4f_other.D1_S3:y_k.C.mean | 1.2133782032610276 | 0.3897453524629424 |
| h4f_other.D1_S3:y_k.C.negative |  | 1 |
| h4f_other.D1_S3:y_k.C.positive | 9 | 4 |
| h4f_other.D1_S3:y_k.C.t_interval_95_descriptive_not_used |  | [-0.49470095710740936, 1.274191662033294] |
| h4f_other.D1_S3:y_k.L.defined | 10 | 5 |
| h4f_other.D1_S3:y_k.L.mean | 2.754276241371183 | 2.3472570527709813 |
| h4f_other.D1_S3:y_k.L.negative |  | 0 |
| h4f_other.D1_S3:y_k.L.positive | 10 | 5 |
| h4f_other.D1_S3:y_k.L.t_interval_95_descriptive_not_used |  | [1.5340665571257566, 3.1604475484162062] |
| h4f_other.D1_S3:y_k.cell |  | D1_S3 |
| h4f_other.D1_S3:y_k.components_defined_ok |  | True |
| h4f_other.D1_S3:y_k.gate_passes |  | True |
| h4f_other.D1_S3:y_k.leave_one_out_rho_A_range |  | [0.33373264716837026, 0.44139151081110245] |
| h4f_other.D1_S3:y_k.per_session.2026-06-01.A |  | 0.8809387793242363 |
| h4f_other.D1_S3:y_k.per_session.2026-06-01.A_over_L |  | 0.3167911730800888 |
| h4f_other.D1_S3:y_k.per_session.2026-06-01.L |  | 2.780818577610822 |
| h4f_other.D1_S3:y_k.per_session.2026-07-01.A |  | 0.49257216714979624 |
| h4f_other.D1_S3:y_k.per_session.2026-07-01.A_over_L |  | 0.31547747537620485 |
| h4f_other.D1_S3:y_k.per_session.2026-07-01.L |  | 1.5613544724941364 |
| h4f_other.D1_S3:y_k.per_session.2026-08-01.A |  | 1.5316326974141092 |
| h4f_other.D1_S3:y_k.per_session.2026-08-01.A_over_L |  | 0.8316771368150109 |
| h4f_other.D1_S3:y_k.per_session.2026-08-01.L |  | 1.841619337138023 |
| h4f_other.D1_S3:y_k.per_session.2026-09-01.A |  | 0.7830285055091757 |
| h4f_other.D1_S3:y_k.per_session.2026-09-01.A_over_L |  | 0.3265509037607802 |
| h4f_other.D1_S3:y_k.per_session.2026-09-01.L |  | 2.39787578748456 |
| h4f_other.D1_S3:y_k.per_session.2026-10-01.A |  | 1.145633600586693 |
| h4f_other.D1_S3:y_k.per_session.2026-10-01.A_over_L |  | 0.36316090613190705 |
| h4f_other.D1_S3:y_k.per_session.2026-10-01.L |  | 3.1546170891273655 |
| h4f_other.D1_S3:y_k.rho_A |  | 0.41186846104286806 |
| h4f_other.D1_S3:y_k.rho_B |  | 0.245837838038115 |
| h4f_other.D1_S3:y_k.status | stress test | stress test |
| h4f_other.D1_S3:y_k.sum_L |  | 11.736285263854906 |
| h4f_other.D1_S3:y_k.target |  | y_k |
| h4f_other.D1_S3:y_view.A.defined | 10 | 5 |
| h4f_other.D1_S3:y_view.A.mean | -0.0037813219922588903 | 0.020141233050729745 |
| h4f_other.D1_S3:y_view.A.negative |  | 1 |
| h4f_other.D1_S3:y_view.A.positive | 6 | 4 |
| h4f_other.D1_S3:y_view.A.t_interval_95_descriptive_not_used |  | [-0.01340079031405417, 0.053683256415513664] |
| h4f_other.D1_S3:y_view.B.defined | 10 | 5 |
| h4f_other.D1_S3:y_view.B.mean | 0.02607629345130933 | 0.01884803360403282 |
| h4f_other.D1_S3:y_view.B.negative |  | 0 |
| h4f_other.D1_S3:y_view.B.positive | 8 | 5 |
| h4f_other.D1_S3:y_view.B.t_interval_95_descriptive_not_used |  | [-0.005745886966653523, 0.04344195417471916] |
| h4f_other.D1_S3:y_view.C.defined | 10 | 5 |
| h4f_other.D1_S3:y_view.C.mean | -0.0282882524548012 | 0.002108982925410352 |
| h4f_other.D1_S3:y_view.C.negative |  | 1 |
| h4f_other.D1_S3:y_view.C.positive | 5 | 4 |
| h4f_other.D1_S3:y_view.C.t_interval_95_descriptive_not_used |  | [-0.055341036866344014, 0.05955900271716472] |
| h4f_other.D1_S3:y_view.L.defined | 10 | 5 |
| h4f_other.D1_S3:y_view.L.mean | 1.5775390281281587 | 2.0559697849866154 |
| h4f_other.D1_S3:y_view.L.negative |  | 0 |
| h4f_other.D1_S3:y_view.L.positive | 10 | 5 |
| h4f_other.D1_S3:y_view.L.t_interval_95_descriptive_not_used |  | [1.0039893866002287, 3.107950183373002] |
| h4f_other.D1_S3:y_view.cell |  | D1_S3 |
| h4f_other.D1_S3:y_view.components_defined_ok |  | True |
| h4f_other.D1_S3:y_view.gate_passes |  | True |
| h4f_other.D1_S3:y_view.leave_one_out_rho_A_range |  | [0.006404836287759596, 0.014510861761541372] |
| h4f_other.D1_S3:y_view.per_session.2026-06-01.A |  | 0.04870643399396091 |
| h4f_other.D1_S3:y_view.per_session.2026-06-01.A_over_L |  | 0.022538568486704234 |
| h4f_other.D1_S3:y_view.per_session.2026-06-01.L |  | 2.1610260661715675 |
| h4f_other.D1_S3:y_view.per_session.2026-07-01.A |  | 0.020409807209897934 |
| h4f_other.D1_S3:y_view.per_session.2026-07-01.A_over_L |  | 0.020527811209552157 |
| h4f_other.D1_S3:y_view.per_session.2026-07-01.L |  | 0.9942515059959578 |
| h4f_other.D1_S3:y_view.per_session.2026-08-01.A |  | -0.024248033430829263 |
| h4f_other.D1_S3:y_view.per_session.2026-08-01.A_over_L |  | -0.014530496262944573 |
| h4f_other.D1_S3:y_view.per_session.2026-08-01.L |  | 1.6687684296555094 |
| h4f_other.D1_S3:y_view.per_session.2026-09-01.A |  | 0.030320874485700866 |
| h4f_other.D1_S3:y_view.per_session.2026-09-01.A_over_L |  | 0.0141369743016839 |
| h4f_other.D1_S3:y_view.per_session.2026-09-01.L |  | 2.1447923607026187 |
| h4f_other.D1_S3:y_view.per_session.2026-10-01.A |  | 0.025517082994918283 |
| h4f_other.D1_S3:y_view.per_session.2026-10-01.A_over_L |  | 0.007706735606534855 |
| h4f_other.D1_S3:y_view.per_session.2026-10-01.L |  | 3.3110105624074233 |
| h4f_other.D1_S3:y_view.rho_A |  | 0.00979646354620959 |
| h4f_other.D1_S3:y_view.rho_B |  | 0.009167466244721843 |
| h4f_other.D1_S3:y_view.status | stress test | stress test |
| h4f_other.D1_S3:y_view.sum_L |  | 10.279848924933077 |
| h4f_other.D1_S3:y_view.target |  | y_view |
| h4f_other.D1_S:y_k.A.defined | 10 | 5 |
| h4f_other.D1_S:y_k.A.mean | 0.5634189173890569 | 0.30540667102341396 |
| h4f_other.D1_S:y_k.A.negative |  | 0 |
| h4f_other.D1_S:y_k.A.positive | 10 | 5 |
| h4f_other.D1_S:y_k.A.t_interval_95_descriptive_not_used |  | [0.14081615553337679, 0.4699971865134511] |
| h4f_other.D1_S:y_k.B.defined | 10 | 5 |
| h4f_other.D1_S:y_k.B.mean | 0.16014099968345805 | 0.23256882056826447 |
| h4f_other.D1_S:y_k.B.negative |  | 1 |
| h4f_other.D1_S:y_k.B.positive | 8 | 4 |
| h4f_other.D1_S:y_k.B.t_interval_95_descriptive_not_used |  | [-0.03302503064391901, 0.49816267178044793] |
| h4f_other.D1_S:y_k.C.defined | 10 | 5 |
| h4f_other.D1_S:y_k.C.mean | 0.4061909848893075 | 0.07373136394858149 |
| h4f_other.D1_S:y_k.C.negative |  | 4 |
| h4f_other.D1_S:y_k.C.positive | 6 | 1 |
| h4f_other.D1_S:y_k.C.t_interval_95_descriptive_not_used |  | [-0.31057235853315196, 0.45803508643031493] |
| h4f_other.D1_S:y_k.L.defined | 10 | 5 |
| h4f_other.D1_S:y_k.L.mean | 0.983781993327262 | 0.855564599397567 |
| h4f_other.D1_S:y_k.L.negative |  | 0 |
| h4f_other.D1_S:y_k.L.positive | 10 | 5 |
| h4f_other.D1_S:y_k.L.t_interval_95_descriptive_not_used |  | [0.546193311961892, 1.164935886833242] |
| h4f_other.D1_S:y_k.cell |  | D1_S |
| h4f_other.D1_S:y_k.components_defined_ok |  | True |
| h4f_other.D1_S:y_k.gate_passes |  | True |
| h4f_other.D1_S:y_k.leave_one_out_rho_A_range |  | [0.2835288736062894, 0.3829473103850725] |
| h4f_other.D1_S:y_k.note |  | Secondary. Largely implied by the target choice (E004 §0, §9); reported against the projection, not as a discovery. |
| h4f_other.D1_S:y_k.per_session.2026-06-01.A |  | 0.2763437682632208 |
| h4f_other.D1_S:y_k.per_session.2026-06-01.A_over_L |  | 0.2731032245473223 |
| h4f_other.D1_S:y_k.per_session.2026-06-01.L |  | 1.011865636962983 |
| h4f_other.D1_S:y_k.per_session.2026-07-01.A |  | 0.12342147014368088 |
| h4f_other.D1_S:y_k.per_session.2026-07-01.A_over_L |  | 0.21334027028161787 |
| h4f_other.D1_S:y_k.per_session.2026-07-01.L |  | 0.5785193296172331 |
| h4f_other.D1_S:y_k.per_session.2026-08-01.A |  | 0.489144939602304 |
| h4f_other.D1_S:y_k.per_session.2026-08-01.A_over_L |  | 0.7925049252662387 |
| h4f_other.D1_S:y_k.per_session.2026-08-01.L |  | 0.6172137535145006 |
| h4f_other.D1_S:y_k.per_session.2026-09-01.A |  | 0.2859793334731413 |
| h4f_other.D1_S:y_k.per_session.2026-09-01.A_over_L |  | 0.31036687494925524 |
| h4f_other.D1_S:y_k.per_session.2026-09-01.L |  | 0.9214235041026808 |
| h4f_other.D1_S:y_k.per_session.2026-10-01.A |  | 0.35214384363472284 |
| h4f_other.D1_S:y_k.per_session.2026-10-01.A_over_L |  | 0.3065316911124331 |
| h4f_other.D1_S:y_k.per_session.2026-10-01.L |  | 1.1488007727904375 |
| h4f_other.D1_S:y_k.projection.L_pp | 0.75 | 0.75 |
| h4f_other.D1_S:y_k.projection.rho_a | 0.37 | 0.37 |
| h4f_other.D1_S:y_k.projection.rho_b | 0.31 | 0.31 |
| h4f_other.D1_S:y_k.rho_A |  | 0.3569650628818227 |
| h4f_other.D1_S:y_k.rho_A_minus_projection | 0.20270708471041476 | -0.01303493711817727 |
| h4f_other.D1_S:y_k.rho_B |  | 0.27183081292987615 |
| h4f_other.D1_S:y_k.status | stress test | stress test |
| h4f_other.D1_S:y_k.sum_L |  | 4.277822996987835 |
| h4f_other.D1_S:y_k.target |  | y_k |
| h4f_other.D2:y_k.A.defined | 10 | 5 |
| h4f_other.D2:y_k.A.mean | 0.001021321567629041 | 0.0012123795009568283 |
| h4f_other.D2:y_k.A.negative |  | 4 |
| h4f_other.D2:y_k.A.positive | 3 | 1 |
| h4f_other.D2:y_k.A.t_interval_95_descriptive_not_used |  | [-0.004242845971111728, 0.006667604973025385] |
| h4f_other.D2:y_k.B.defined | 10 | 5 |
| h4f_other.D2:y_k.B.mean | -0.0007669808895260477 | -0.0002234064512605549 |
| h4f_other.D2:y_k.B.negative |  | 2 |
| h4f_other.D2:y_k.B.positive | 3 | 3 |
| h4f_other.D2:y_k.B.t_interval_95_descriptive_not_used |  | [-0.0021357763093061946, 0.0016889634067850847] |
| h4f_other.D2:y_k.C.defined | 10 | 5 |
| h4f_other.D2:y_k.C.mean | 0.002879245388106533 | 0.00031730943990373464 |
| h4f_other.D2:y_k.C.negative |  | 4 |
| h4f_other.D2:y_k.C.positive | 5 | 1 |
| h4f_other.D2:y_k.C.t_interval_95_descriptive_not_used |  | [-0.0034124581732598853, 0.004047077053067355] |
| h4f_other.D2:y_k.L.defined | 10 | 5 |
| h4f_other.D2:y_k.L.mean | 0.004256753325388951 | 0.0048376670785302165 |
| h4f_other.D2:y_k.L.negative |  | 1 |
| h4f_other.D2:y_k.L.positive | 7 | 4 |
| h4f_other.D2:y_k.L.t_interval_95_descriptive_not_used |  | [0.00038498429134739033, 0.009290349865713043] |
| h4f_other.D2:y_k.cell |  | D2 |
| h4f_other.D2:y_k.components_defined_ok |  | True |
| h4f_other.D2:y_k.gate_passes |  | False |
| h4f_other.D2:y_k.leave_one_out_rho_A_range |  | [-0.138619047874489, 0.42994519068409875] |
| h4f_other.D2:y_k.per_session.2026-06-01.A |  | -0.0011332173980864724 |
| h4f_other.D2:y_k.per_session.2026-06-01.A_over_L |  | -0.18896444169867302 |
| h4f_other.D2:y_k.per_session.2026-06-01.L |  | 0.005996987517331576 |
| h4f_other.D2:y_k.per_session.2026-07-01.A |  | -0.0010581074229021326 |
| h4f_other.D2:y_k.per_session.2026-07-01.A_over_L |  | 21.01581082947101 |
| h4f_other.D2:y_k.per_session.2026-07-01.L |  | -5.034816079607651e-05 |
| h4f_other.D2:y_k.per_session.2026-08-01.A |  | 0.009046599397266597 |
| h4f_other.D2:y_k.per_session.2026-08-01.A_over_L |  | 3.405267322169249 |
| h4f_other.D2:y_k.per_session.2026-08-01.L |  | 0.002656648815313467 |
| h4f_other.D2:y_k.per_session.2026-09-01.A |  | -0.0004127470902943742 |
| h4f_other.D2:y_k.per_session.2026-09-01.A_over_L |  | -0.06468129078156822 |
| h4f_other.D2:y_k.per_session.2026-09-01.L |  | 0.006381243869857833 |
| h4f_other.D2:y_k.per_session.2026-10-01.A |  | -0.0003806299811994762 |
| h4f_other.D2:y_k.per_session.2026-10-01.A_over_L |  | -0.041355727266861333 |
| h4f_other.D2:y_k.per_session.2026-10-01.L |  | 0.009203803350944284 |
| h4f_other.D2:y_k.rho_A |  | 0.25061242976752635 |
| h4f_other.D2:y_k.rho_B |  | -0.04618061715161069 |
| h4f_other.D2:y_k.status | stress test | stress test |
| h4f_other.D2:y_k.sum_L |  | 0.024188335392651084 |
| h4f_other.D2:y_k.target |  | y_k |
| h4f_other.D2:y_view.A.defined | 10 | 5 |
| h4f_other.D2:y_view.A.mean | 0.001021321567629041 | 0.0012123795009568283 |
| h4f_other.D2:y_view.A.negative |  | 4 |
| h4f_other.D2:y_view.A.positive | 3 | 1 |
| h4f_other.D2:y_view.A.t_interval_95_descriptive_not_used |  | [-0.004242845971111728, 0.006667604973025385] |
| h4f_other.D2:y_view.B.defined | 10 | 5 |
| h4f_other.D2:y_view.B.mean | -0.0007669808895260477 | -0.0002234064512605549 |
| h4f_other.D2:y_view.B.negative |  | 2 |
| h4f_other.D2:y_view.B.positive | 3 | 3 |
| h4f_other.D2:y_view.B.t_interval_95_descriptive_not_used |  | [-0.0021357763093061946, 0.0016889634067850847] |
| h4f_other.D2:y_view.C.defined | 10 | 5 |
| h4f_other.D2:y_view.C.mean | 0.002879245388106533 | 0.00031730943990373464 |
| h4f_other.D2:y_view.C.negative |  | 4 |
| h4f_other.D2:y_view.C.positive | 5 | 1 |
| h4f_other.D2:y_view.C.t_interval_95_descriptive_not_used |  | [-0.0034124581732598853, 0.004047077053067355] |
| h4f_other.D2:y_view.L.defined | 10 | 5 |
| h4f_other.D2:y_view.L.mean | 0.004256753325388951 | 0.0048376670785302165 |
| h4f_other.D2:y_view.L.negative |  | 1 |
| h4f_other.D2:y_view.L.positive | 7 | 4 |
| h4f_other.D2:y_view.L.t_interval_95_descriptive_not_used |  | [0.00038498429134739033, 0.009290349865713043] |
| h4f_other.D2:y_view.cell |  | D2 |
| h4f_other.D2:y_view.components_defined_ok |  | True |
| h4f_other.D2:y_view.gate_passes |  | False |
| h4f_other.D2:y_view.leave_one_out_rho_A_range |  | [-0.138619047874489, 0.42994519068409875] |
| h4f_other.D2:y_view.per_session.2026-06-01.A |  | -0.0011332173980864724 |
| h4f_other.D2:y_view.per_session.2026-06-01.A_over_L |  | -0.18896444169867302 |
| h4f_other.D2:y_view.per_session.2026-06-01.L |  | 0.005996987517331576 |
| h4f_other.D2:y_view.per_session.2026-07-01.A |  | -0.0010581074229021326 |
| h4f_other.D2:y_view.per_session.2026-07-01.A_over_L |  | 21.01581082947101 |
| h4f_other.D2:y_view.per_session.2026-07-01.L |  | -5.034816079607651e-05 |
| h4f_other.D2:y_view.per_session.2026-08-01.A |  | 0.009046599397266597 |
| h4f_other.D2:y_view.per_session.2026-08-01.A_over_L |  | 3.405267322169249 |
| h4f_other.D2:y_view.per_session.2026-08-01.L |  | 0.002656648815313467 |
| h4f_other.D2:y_view.per_session.2026-09-01.A |  | -0.0004127470902943742 |
| h4f_other.D2:y_view.per_session.2026-09-01.A_over_L |  | -0.06468129078156822 |
| h4f_other.D2:y_view.per_session.2026-09-01.L |  | 0.006381243869857833 |
| h4f_other.D2:y_view.per_session.2026-10-01.A |  | -0.0003806299811994762 |
| h4f_other.D2:y_view.per_session.2026-10-01.A_over_L |  | -0.041355727266861333 |
| h4f_other.D2:y_view.per_session.2026-10-01.L |  | 0.009203803350944284 |
| h4f_other.D2:y_view.rho_A |  | 0.25061242976752635 |
| h4f_other.D2:y_view.rho_B |  | -0.04618061715161069 |
| h4f_other.D2:y_view.status | stress test | stress test |
| h4f_other.D2:y_view.sum_L |  | 0.024188335392651084 |
| h4f_other.D2:y_view.target |  | y_view |
| h4f_other.D3:y_k.A.defined | 10 | 5 |
| h4f_other.D3:y_k.A.mean | 0.5614040032678635 | 0.3050716668222611 |
| h4f_other.D3:y_k.A.negative |  | 0 |
| h4f_other.D3:y_k.A.positive | 10 | 5 |
| h4f_other.D3:y_k.A.t_interval_95_descriptive_not_used |  | [0.14120441982704476, 0.46893891381747743] |
| h4f_other.D3:y_k.B.defined | 10 | 5 |
| h4f_other.D3:y_k.B.mean | 0.15968440382002855 | 0.2332663334781418 |
| h4f_other.D3:y_k.B.negative |  | 1 |
| h4f_other.D3:y_k.B.positive | 8 | 4 |
| h4f_other.D3:y_k.B.t_interval_95_descriptive_not_used |  | [-0.03254707791498279, 0.4990797448712664] |
| h4f_other.D3:y_k.C.defined | 10 | 5 |
| h4f_other.D3:y_k.C.mean | 0.4046440987754507 | 0.07266138926727254 |
| h4f_other.D3:y_k.C.negative |  | 4 |
| h4f_other.D3:y_k.C.positive | 6 | 1 |
| h4f_other.D3:y_k.C.t_interval_95_descriptive_not_used |  | [-0.3095978409246346, 0.4549206194591797] |
| h4f_other.D3:y_k.L.defined | 10 | 5 |
| h4f_other.D3:y_k.L.mean | 0.9821784086010131 | 0.8529678312778468 |
| h4f_other.D3:y_k.L.negative |  | 0 |
| h4f_other.D3:y_k.L.positive | 10 | 5 |
| h4f_other.D3:y_k.L.t_interval_95_descriptive_not_used |  | [0.5401863505898533, 1.1657493119658402] |
| h4f_other.D3:y_k.cell |  | D3 |
| h4f_other.D3:y_k.components_defined_ok |  | True |
| h4f_other.D3:y_k.gate_passes |  | True |
| h4f_other.D3:y_k.leave_one_out_rho_A_range |  | [0.28421179811748626, 0.3841481415298115] |
| h4f_other.D3:y_k.note |  | Secondary. Largely implied by the target choice (E004 §0, §9); reported against the projection, not as a discovery. |
| h4f_other.D3:y_k.per_session.2026-06-01.A |  | 0.27671308594968735 |
| h4f_other.D3:y_k.per_session.2026-06-01.A_over_L |  | 0.27278154309020763 |
| h4f_other.D3:y_k.per_session.2026-06-01.L |  | 1.0144127891313364 |
| h4f_other.D3:y_k.per_session.2026-07-01.A |  | 0.12250362700123585 |
| h4f_other.D3:y_k.per_session.2026-07-01.A_over_L |  | 0.21274049192310696 |
| h4f_other.D3:y_k.per_session.2026-07-01.L |  | 0.5758359675388625 |
| h4f_other.D3:y_k.per_session.2026-08-01.A |  | 0.48609739348079994 |
| h4f_other.D3:y_k.per_session.2026-08-01.A_over_L |  | 0.7992437810261616 |
| h4f_other.D3:y_k.per_session.2026-08-01.L |  | 0.608196654163129 |
| h4f_other.D3:y_k.per_session.2026-09-01.A |  | 0.2859941615605548 |
| h4f_other.D3:y_k.per_session.2026-09-01.A_over_L |  | 0.311200263432789 |
| h4f_other.D3:y_k.per_session.2026-09-01.L |  | 0.919003597252166 |
| h4f_other.D3:y_k.per_session.2026-10-01.A |  | 0.35405006611902756 |
| h4f_other.D3:y_k.per_session.2026-10-01.A_over_L |  | 0.30856990243679727 |
| h4f_other.D3:y_k.per_session.2026-10-01.L |  | 1.1473901483037405 |
| h4f_other.D3:y_k.projection.L_pp | 0.75 | 0.75 |
| h4f_other.D3:y_k.projection.rho_a | 0.37 | 0.37 |
| h4f_other.D3:y_k.projection.rho_b | 0.31 | 0.31 |
| h4f_other.D3:y_k.rho_A |  | 0.35765905305623025 |
| h4f_other.D3:y_k.rho_A_minus_projection | 0.20159065842987878 | -0.012340946943769748 |
| h4f_other.D3:y_k.rho_B |  | 0.27347612058086784 |
| h4f_other.D3:y_k.status | stress test | stress test |
| h4f_other.D3:y_k.sum_L |  | 4.264839156389234 |
| h4f_other.D3:y_k.target |  | y_k |
| h4f_other.D4:y_k.A.defined | 10 | 5 |
| h4f_other.D4:y_k.A.mean | 0.10244582135750302 | 0.06616835169519711 |
| h4f_other.D4:y_k.A.negative |  | 2 |
| h4f_other.D4:y_k.A.positive | 6 | 3 |
| h4f_other.D4:y_k.A.t_interval_95_descriptive_not_used |  | [-0.11540379629262892, 0.24774049968302314] |
| h4f_other.D4:y_k.B.defined | 10 | 5 |
| h4f_other.D4:y_k.B.mean | 0.00878176987888053 | 0.042318966395929095 |
| h4f_other.D4:y_k.B.negative |  | 0 |
| h4f_other.D4:y_k.B.positive | 8 | 5 |
| h4f_other.D4:y_k.B.t_interval_95_descriptive_not_used |  | [-0.010873864999519027, 0.09551179779137722] |
| h4f_other.D4:y_k.C.defined | 10 | 5 |
| h4f_other.D4:y_k.C.mean | 0.09270308556411541 | 0.023399074198708725 |
| h4f_other.D4:y_k.C.negative |  | 4 |
| h4f_other.D4:y_k.C.positive | 5 | 1 |
| h4f_other.D4:y_k.C.t_interval_95_descriptive_not_used |  | [-0.10412720618079789, 0.15092535457821535] |
| h4f_other.D4:y_k.L.defined | 10 | 5 |
| h4f_other.D4:y_k.L.mean | 0.24492817168364717 | 0.3706244800027102 |
| h4f_other.D4:y_k.L.negative |  | 0 |
| h4f_other.D4:y_k.L.positive | 10 | 5 |
| h4f_other.D4:y_k.L.t_interval_95_descriptive_not_used |  | [0.013499971847549419, 0.7277489881578709] |
| h4f_other.D4:y_k.cell |  | D4 |
| h4f_other.D4:y_k.components_defined_ok |  | True |
| h4f_other.D4:y_k.gate_passes |  | True |
| h4f_other.D4:y_k.leave_one_out_rho_A_range |  | [0.004918148180345844, 0.21076800045209826] |
| h4f_other.D4:y_k.per_session.2026-06-01.A |  | -0.00825016664347622 |
| h4f_other.D4:y_k.per_session.2026-06-01.A_over_L |  | -0.03377302773820478 |
| h4f_other.D4:y_k.per_session.2026-06-01.L |  | 0.2442827071184812 |
| h4f_other.D4:y_k.per_session.2026-07-01.A |  | -0.02020988031242732 |
| h4f_other.D4:y_k.per_session.2026-07-01.A_over_L |  | -0.1459978709990547 |
| h4f_other.D4:y_k.per_session.2026-07-01.L |  | 0.1384258563096319 |
| h4f_other.D4:y_k.per_session.2026-08-01.A |  | 0.326013283446247 |
| h4f_other.D4:y_k.per_session.2026-08-01.A_over_L |  | 0.3741449714232006 |
| h4f_other.D4:y_k.per_session.2026-08-01.L |  | 0.8713555128273764 |
| h4f_other.D4:y_k.per_session.2026-09-01.A |  | 0.009151292146614587 |
| h4f_other.D4:y_k.per_session.2026-09-01.A_over_L |  | 0.031541784507223405 |
| h4f_other.D4:y_k.per_session.2026-09-01.L |  | 0.2901323526739219 |
| h4f_other.D4:y_k.per_session.2026-10-01.A |  | 0.02413722983902744 |
| h4f_other.D4:y_k.per_session.2026-10-01.A_over_L |  | 0.07813273113400161 |
| h4f_other.D4:y_k.per_session.2026-10-01.L |  | 0.30892597108413966 |
| h4f_other.D4:y_k.rho_A |  | 0.17853205944386955 |
| h4f_other.D4:y_k.rho_B |  | 0.1141828688585806 |
| h4f_other.D4:y_k.status | stress test | stress test |
| h4f_other.D4:y_k.sum_L |  | 1.853122400013551 |
| h4f_other.D4:y_k.target |  | y_k |
| h4f_other.D4:y_view.A.defined | 10 | 5 |
| h4f_other.D4:y_view.A.mean | 0.10244582135750302 | 0.06616835169519711 |
| h4f_other.D4:y_view.A.negative |  | 2 |
| h4f_other.D4:y_view.A.positive | 6 | 3 |
| h4f_other.D4:y_view.A.t_interval_95_descriptive_not_used |  | [-0.11540379629262892, 0.24774049968302314] |
| h4f_other.D4:y_view.B.defined | 10 | 5 |
| h4f_other.D4:y_view.B.mean | 0.00878176987888053 | 0.042318966395929095 |
| h4f_other.D4:y_view.B.negative |  | 0 |
| h4f_other.D4:y_view.B.positive | 8 | 5 |
| h4f_other.D4:y_view.B.t_interval_95_descriptive_not_used |  | [-0.010873864999519027, 0.09551179779137722] |
| h4f_other.D4:y_view.C.defined | 10 | 5 |
| h4f_other.D4:y_view.C.mean | 0.09270308556411541 | 0.023399074198708725 |
| h4f_other.D4:y_view.C.negative |  | 4 |
| h4f_other.D4:y_view.C.positive | 5 | 1 |
| h4f_other.D4:y_view.C.t_interval_95_descriptive_not_used |  | [-0.10412720618079789, 0.15092535457821535] |
| h4f_other.D4:y_view.L.defined | 10 | 5 |
| h4f_other.D4:y_view.L.mean | 0.24492817168364717 | 0.3706244800027102 |
| h4f_other.D4:y_view.L.negative |  | 0 |
| h4f_other.D4:y_view.L.positive | 10 | 5 |
| h4f_other.D4:y_view.L.t_interval_95_descriptive_not_used |  | [0.013499971847549419, 0.7277489881578709] |
| h4f_other.D4:y_view.cell |  | D4 |
| h4f_other.D4:y_view.components_defined_ok |  | True |
| h4f_other.D4:y_view.gate_passes |  | True |
| h4f_other.D4:y_view.leave_one_out_rho_A_range |  | [0.004918148180345844, 0.21076800045209826] |
| h4f_other.D4:y_view.per_session.2026-06-01.A |  | -0.00825016664347622 |
| h4f_other.D4:y_view.per_session.2026-06-01.A_over_L |  | -0.03377302773820478 |
| h4f_other.D4:y_view.per_session.2026-06-01.L |  | 0.2442827071184812 |
| h4f_other.D4:y_view.per_session.2026-07-01.A |  | -0.02020988031242732 |
| h4f_other.D4:y_view.per_session.2026-07-01.A_over_L |  | -0.1459978709990547 |
| h4f_other.D4:y_view.per_session.2026-07-01.L |  | 0.1384258563096319 |
| h4f_other.D4:y_view.per_session.2026-08-01.A |  | 0.326013283446247 |
| h4f_other.D4:y_view.per_session.2026-08-01.A_over_L |  | 0.3741449714232006 |
| h4f_other.D4:y_view.per_session.2026-08-01.L |  | 0.8713555128273764 |
| h4f_other.D4:y_view.per_session.2026-09-01.A |  | 0.009151292146614587 |
| h4f_other.D4:y_view.per_session.2026-09-01.A_over_L |  | 0.031541784507223405 |
| h4f_other.D4:y_view.per_session.2026-09-01.L |  | 0.2901323526739219 |
| h4f_other.D4:y_view.per_session.2026-10-01.A |  | 0.02413722983902744 |
| h4f_other.D4:y_view.per_session.2026-10-01.A_over_L |  | 0.07813273113400161 |
| h4f_other.D4:y_view.per_session.2026-10-01.L |  | 0.30892597108413966 |
| h4f_other.D4:y_view.rho_A |  | 0.17853205944386955 |
| h4f_other.D4:y_view.rho_B |  | 0.1141828688585806 |
| h4f_other.D4:y_view.status | stress test | stress test |
| h4f_other.D4:y_view.sum_L |  | 1.853122400013551 |
| h4f_other.D4:y_view.target |  | y_view |
| status |  | modeled historical replay under stress test; LP tier 4 fees hypothetical, not attainable |


