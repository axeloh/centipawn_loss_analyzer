# Centipawn Loss Analyzer 
Jumping on the chess-cheating-scandal bandwagon and analyzing the ACPL (Average CentiPawn Loss) over time for a selected set of 25+ GMs.  
  - Games were filtered to only include OTB classical games (no online games, no bullet, blitz or rapid, no simuls, no blindfolds)
  - Opening moves (first 10) were filtered out
  - Short games (less than 10 moves after the opening moves) were filtered out
  - Games were analyzed using Stockfish 15 with depth 15

**TLDR;** 
  - Nothing suspicious found with regards to Niemann's ELO vs ACPL.
  - Statistical analysis cannot be trusted for a player where the number of games within certain ELO intervals is substantially underrepresented.

Here follows numerous plots of the findings...

---
#### Number of games analyzed per player 
![](plots/num_games_per_player.png)

---
#### ACPL distribution across all players
![](plots/acpl_total_distribution.png)

---
#### ACPL distribution per player (boxplot)
![](plots/acpl_distribution_per_player.png)

---
#### ELO vs ACPL trend across all players
![](plots/elo_vs_acpl_total_trend.png)

---
#### ELO vs ACPL trend per player 
![](plots/elo_vs_acpl_per_player.png)

---

As a player's rating is not distributed evenly, but rather in a stepwise manner, it makes sense to group them into tiers (buckets) for certain stastistical analysis. Here I'm using a bucket size representing 50 ELO points.

#### Total number of games per tier
![](plots/num_games_per_tier.png)

---
#### Number of games per tier per player
![](plots/num_games_per_tier_per_player.png)

---
#### Overall ELO (tier) vs ACPL
![](plots/tier_elo_vs_acpl_total.png)

---
#### ELO (tier) vs ACPL per player
![](plots/tier_elo_vs_acpl_anand.png)
![](plots/tier_elo_vs_acpl_aronian.png)
![](plots/tier_elo_vs_acpl_carlsen.png)
![](plots/tier_elo_vs_acpl_caruana.png)
![](plots/tier_elo_vs_acpl_ding.png)
![](plots/tier_elo_vs_acpl_duda.png)
![](plots/tier_elo_vs_acpl_firouzja.png)
![](plots/tier_elo_vs_acpl_giri.png)
![](plots/tier_elo_vs_acpl_grischuk.png)
![](plots/tier_elo_vs_acpl_gukesh.png)
![](plots/tier_elo_vs_acpl_jobava.png)
![](plots/tier_elo_vs_acpl_karjakin.png)
![](plots/tier_elo_vs_acpl_keymer.png)
![](plots/tier_elo_vs_acpl_nakamura.png)
![](plots/tier_elo_vs_acpl_nepo.png)
![](plots/tier_elo_vs_acpl_niemann.png)
![](plots/tier_elo_vs_acpl_polgar.png)
![](plots/tier_elo_vs_acpl_pragg.png)
![](plots/tier_elo_vs_acpl_rapport.png)
![](plots/tier_elo_vs_acpl_sarin.png)
![](plots/tier_elo_vs_acpl_so.png)

---
#### Fraction of games with ACPL sub x % 
![](plots/fraction_games_acpl_sub_30.png)
![](plots/fraction_games_acpl_sub_20.png)
![](plots/fraction_games_acpl_sub_15.png)
![](plots/fraction_games_acpl_sub_10.png)
![](plots/fraction_games_acpl_sub_5.png)
![](plots/fraction_games_acpl_sub_3.png)
![](plots/fraction_games_acpl_sub_1.png)


