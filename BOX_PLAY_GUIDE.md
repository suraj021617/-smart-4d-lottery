# 🎯 BOX PLAY QUICK REFERENCE GUIDE

## What is Box Play?

Box Play means playing all permutations (different arrangements) of your 4D number.

**Example:**
- Main Number: **7221**
- Box Combinations: 1227, 1272, 1722, 2127, 2172, 2217, 2271, 2712, 2721, 7122, 7212, 7221
- If ANY of these combinations wins, you win!

---

## How to Use

### Step 1: Go to Quick Pick
```
URL: http://127.0.0.1:5000/quick-pick
```

### Step 2: See Your 5 Numbers
- Top section shows your main predictions
- Each with confidence percentage

### Step 3: Scroll Down to BOX PLAY Section
- Shows all backup options
- Displays permutations for each number

### Step 4: Choose Your Strategy

**Strategy A: Play Main Only**
- Play just the 5 main numbers
- Highest confidence (95%)
- Lowest cost

**Strategy B: Play Main + Box**
- Play main numbers
- Also play top 6 permutations
- Medium cost, better coverage

**Strategy C: Play All Permutations**
- Play all possible permutations
- Highest cost, maximum coverage
- Guaranteed win if any permutation matches

---

## Understanding the Stats

### Box Hit Rate
- **33.3%** = 4 out of 12 permutations appeared in last 100 draws
- Higher = Better (more likely to hit)
- Strong: >30%, Moderate: 15-30%, Weak: <15%

### 3-Digit Matches
- Count of times 3 out of 4 digits matched
- Fallback if 4-digit misses
- Example: You play 7221, but 7212 comes (3 digits match)

### iBox Matches
- Count of times first 3 digits matched
- Example: You play 7221, but 7245 comes (first 3 digits: 724 vs 722 - no match)
- Rare but possible

### Backup Options
- Alternative permutations to play
- Lower confidence than main
- Use if main numbers miss

---

## Example Breakdown

```
YOUR 5 LUCKY NUMBERS
┌─────────────────────────────────────┐
│ 5042  5050  0428  3504  1504        │
│ 95%   95%   95%   95%   95%         │
└─────────────────────────────────────┘

📦 BOX PLAY BACKUP OPTIONS

Number 1: 5042
├─ Box Hit Rate: 25.5%
├─ Permutations: 0245, 0254, 0425, 0452, 0524, 0542
├─ Backup Options: 2045, 5420, 4025
├─ 3-Digit Matches: 8 times
├─ iBox Matches: 3 times
└─ Recommendation: Moderate

Number 2: 5050
├─ Box Hit Rate: 16.7%
├─ Permutations: 0055, 0505, 0550, 5005, 5050, 5500
├─ Backup Options: 0550, 5500, 5005
├─ 3-Digit Matches: 5 times
├─ iBox Matches: 2 times
└─ Recommendation: Moderate

... (3 more numbers)
```

---

## Cost Calculation

### Example: Playing 5 Numbers

**Main Only:**
- 5 numbers × RM1 = **RM5**

**Main + Box (6 perms each):**
- 5 main × RM1 = RM5
- 5 × 6 perms × RM1 = RM30
- **Total: RM35**

**All Permutations:**
- 5 × 24 perms × RM1 = **RM120**

---

## Winning Scenarios

### Scenario 1: Main Number Wins
- You play: 7221
- Result: 7221 ✅ WIN
- Payout: Full prize

### Scenario 2: Box Permutation Wins
- You play: 7221 (main) + 1227, 1272, 1722, 2127, 2172, 2217 (box)
- Result: 2172 ✅ WIN
- Payout: Full prize (because 2172 is a permutation of 7221)

### Scenario 3: 3-Digit Match
- You play: 7221
- Result: 7212 (3 digits match: 7, 2, 2)
- Payout: Partial (if lottery offers 3-digit prize)

### Scenario 4: Miss
- You play: 7221
- Result: 1234 ❌ MISS
- Payout: None

---

## Pro Tips

✅ **Tip 1: Check Box Hit Rate**
- Strong (>30%): Play all 6 permutations
- Moderate (15-30%): Play top 3 permutations
- Weak (<15%): Play main only

✅ **Tip 2: Use Backup Options**
- If main misses, try backup options
- Lower confidence but still worth trying

✅ **Tip 3: Track 3-Digit Matches**
- High 3-digit matches = number is "hot"
- Consider playing more permutations

✅ **Tip 4: Combine Strategies**
- Play main numbers from Quick Pick
- Use box play as backup
- Use 3-digit matches as last resort

✅ **Tip 5: Budget Wisely**
- Start with main only (RM5)
- Add box play if budget allows (RM35)
- Don't play all permutations unless confident

---

## FAQ

**Q: What's the difference between Box and iBox?**
A: Box = any permutation wins. iBox = first 3 digits must match (more restrictive).

**Q: Should I play all permutations?**
A: Only if box hit rate is >30% and you have budget. Otherwise, play top 6.

**Q: Can I win with 3-digit match?**
A: Depends on lottery. Some offer 3-digit prizes, some don't.

**Q: How many permutations does a 4D number have?**
A: Up to 24 (if all digits different). Less if digits repeat.

**Q: Is box play worth it?**
A: Yes! If box hit rate >20%, you have better coverage for same cost.

---

## Next Draw Prediction

**Date:** {{ next_draw_date }}
**Provider:** {{ provider_name }}
**Numbers:** {{ numbers|join(', ') }}
**Strategy:** Main + Box (Recommended)
**Estimated Cost:** RM35 (5 main + 30 box)

---

**Good Luck! 🍀**
