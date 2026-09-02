# GPU Component Salvage: Secondary Market Reality Check

**Date:** 2026-03-29

## Purpose

The 22 scrap/salvage reports assign "component salvage (theoretical max)" values to
individual GPU subcomponents -- e.g., $800 for an H100 die (reballing/rework), $1,200 for
HBM3 stacks, $165 for VRM power stages. These figures assume a buyer exists for each
component at those prices. This document investigates whether those buyers actually exist.

**Bottom line:** Component-level salvage is real for a narrow set of parts (power modules,
coolers, connectors, individual VRAM chips) in a narrow set of geographies (primarily
Shenzhen). It is not a scalable or predictable recovery path for most GPU end-of-life
scenarios. The reports' "theoretical max" figures overstate realistically recoverable value
by 3-10x.

---

## 1. GPU Die (Bare Silicon)

### What the reports assume
- H100 GH100 die: $800 secondary market (reballing/rework for refurbishment)
- A100 GA100 die: $150 secondary market
- Consumer dies (AD102, GA102): implied value from stripped-card economics

### What actually exists

**The Shenzhen gray market is real but geographically constrained.**

Underground repair shops in Shenzhen service banned NVIDIA accelerators (A100, H100) at
scale. Reuters and Tom's Hardware report ~12 firms operating as of late 2024, with the
largest handling 500 repairs/month. They charge $1,400-$2,800 per GPU repair (roughly 10%
of retail value). These shops do harvest dies and HBM from dead donor cards to repair
others.

However:
- This market exists specifically because of US export controls creating artificial scarcity
  in China. It is not a general global market.
- The shops are buying *whole dead cards* as donors, not individual bare dies.
- A bare desoldered die with no provenance, no test data, and unknown failure history has
  near-zero value outside this ecosystem.
- Die reballing requires $100,000+ BGA rework stations with chip-specific stencils.
  Only a handful of shops globally have both the equipment and the expertise.

**The RTX 4090 die-stripping phenomenon confirms die value -- but only in a sanctions-driven context.**

Chinese operations buy RTX 4090 cards in bulk, surgically remove the AD102 die and all
24 GDDR6X VRAM chips, and mount them on custom PCBs with blower coolers for resale to AI
firms. The stripped donor cards then appear on eBay/Facebook Marketplace for ~$200 (vs.
~$2,200 working). This means the die + VRAM extraction is worth roughly $2,000 to these
operations -- but this value is driven by:
1. The China AI chip ban making AD102 dies irreplaceable
2. Custom PCB infrastructure that does not exist outside Shenzhen
3. Bulk purchasing at scale (not individual card economics)

Sources:
- [Tom's Hardware: Stripped RTX 4090](https://www.tomshardware.com/pc-components/gpus/used-rtx-4090-from-ebay-shows-up-with-no-gpu-chip-or-video-memory-stripped-asus-tuf-rtx-4090-points-to-increasing-number-of-scams-in-the-used-gpu-market)
- [Tom's Hardware: Underground China repair shops](https://www.tomshardware.com/pc-components/gpus/underground-china-repair-shops-thrive-servicing-illicit-nvidia-gpus-banned-by-export-restrictions-companies-resurrecting-banned-ai-accelerators-at-a-rate-of-up-to-500-per-month)
- [TechRadar: China surge in unauthorized AI chip repairs](https://www.techradar.com/pro/potentially-tens-of-thousands-of-faulty-nvidia-ai-chips-end-up-in-these-obscure-chinese-repair-shops-it-may-mask-something-even-more-vital)
- [GamersNexus: NVIDIA AI GPU Black Market](https://gamersnexus.net/gpus-deep-dive-news/nvidia-ai-gpu-black-market-investigating-smuggling-corruption-governments)

### Realistic value of a bare GPU die

| Context | Die value |
|---------|-----------|
| Shenzhen gray-market donor (tested, known-good) | $200-$800 for datacenter dies |
| Shenzhen gray-market donor (consumer AD102) | Implied ~$500-$1,000 from stripped-card economics |
| Western repair shop (NorthridgeFix, ZapFixers, etc.) | Near $0 -- shops buy whole dead cards, not bare dies |
| E-waste recycler | $0.004-$0.05 (silicon scrap at ~$5/kg) |
| General secondary market (eBay, broker) | No listings found. No liquid market exists. |

**Report overstatement factor:** The H100 die at $800 is plausible only if sold into the
Shenzhen gray market and only if sanctions persist. For a Western decommission scenario, the
realistic value is near zero. **3-200x overstatement depending on context.**

---

## 2. HBM Stacks (HBM2e, HBM3, HBM3e)

### What the reports assume
- H100 SXM5: $1,200 total ($240/stack x 5 active stacks)
- A100 SXM4: $300 total ($60/stack x 5 stacks)

### What actually exists

**Individual HBM stacks are not sold anywhere.**

Exhaustive searching of eBay, AliExpress, Taobao (via web search), Mouser, DigiKey, and
Octopart returned zero listings for individual HBM2e, HBM3, or HBM3e memory stacks.

This is expected because:
- HBM is sold by SK Hynix, Samsung, and Micron exclusively to OEMs (NVIDIA, AMD, Intel)
  under long-term supply contracts.
- HBM stacks are bonded to a silicon interposer using microbumps and underfill epoxy
  (CoWoS or equivalent packaging). Non-destructive removal requires TSMC/OSAT-grade
  equipment that does not exist in the repair ecosystem.
- Even if removed intact, an HBM stack requires a silicon interposer, microbump interface,
  and known-good-die (KGD) testing infrastructure to be useful. There is no plug-and-play
  application.
- The $240/stack figure in the H100 report derives from "$15/GB at 2025 HBM3 contract
  pricing" -- but this is the price NVIDIA pays SK Hynix for new, tested, KGD stacks
  delivered with full warranty. A desoldered stack of unknown provenance has none of these
  attributes.

The Shenzhen repair shops that service H100s may swap HBM stacks between boards, but this
is done at the card level (dead card as donor -> working card as recipient), not by trading
individual stacks.

### Realistic value of desoldered HBM stacks

| Context | Value |
|---------|-------|
| Shenzhen donor-card repair (implicit, as part of whole card) | Unknowable -- bundled with die |
| Individual stack, any marketplace | $0. No market exists. |
| E-waste recycler | $0.10/stack (Cu microbumps and trace Au) |

**Report overstatement factor:** Effectively infinite. The $240/stack and $60/stack figures
assume a market that does not exist. **Realistic standalone value: $0.**

---

## 3. VRAM Chips (GDDR6, GDDR6X, GDDR7)

### What the reports assume
The reports do not break out individual VRAM chip value for consumer cards, but the
stripped-RTX-4090 phenomenon implies they have meaningful value.

### What actually exists

**Individual GDDR6/GDDR6X chips are sold on AliExpress and used in GPU repair.**

This is the one component category where a real, liquid, retail market exists:

- AliExpress sellers (e.g., Shenzhen Hong Ming Electronics Co.) sell individual GDDR6 and
  GDDR6X chips for $5-$20 per chip depending on part number, speed, and density.
- A Samsung K4ZAF325BM-HC14 (GDDR6, 2GB, 180-FBGA) was listed at ~$15 on AliExpress.
- Spot market pricing (DRAMeXchange): 8Gb GDDR6 IC dropped from ~$13 (Feb 2022) to ~$3.36
  (mid-2023). GDDR6X pricing is higher but not publicly listed by Micron.
- GPU repair shops (ZapFixers, NorthridgeFix, Shenzhen repair ecosystem) actively source
  individual VRAM chips for board-level repair.
- Some repair techs harvest VRAM from donor cards (dead cards with intact memory) rather
  than buying new chips.

**However, the demand side is tiny.** VRAM chip replacement is a niche repair operation
requiring professional BGA rework equipment. The total addressable market for individual
VRAM chips is the global GPU repair industry -- perhaps a few thousand technicians worldwide.

### Realistic value

| Component | Price per chip |
|-----------|---------------|
| GDDR6 1GB (8Gb) new, AliExpress | $3-$8 |
| GDDR6 2GB (16Gb) new, AliExpress | $8-$15 |
| GDDR6X 2GB (Micron, AliExpress) | $10-$20 |
| Harvested/desoldered chip (unknown condition) | $1-$5 (significant discount for no test data) |

For a full RTX 4090 (24x 1GB GDDR6X chips): ~$240-$480 if all chips are intact and tested.
This is consistent with the stripped-card economics (card worth ~$2,200 working, stripped
shell sold for ~$200, implying die + VRAM worth ~$2,000).

Sources:
- [AliExpress: GDDR6X memory chips](https://www.aliexpress.com/w/wholesale-gddr6x-memory-chip.html)
- [Tom's Hardware: GDDR6 prices plummet](https://www.tomshardware.com/news/gddr6-vram-prices-plummet)
- [RupZ Blog: VRAM chip replacement](https://rupz.me/electronics/graphics-card-vram-chip-replacement-procedure/)

---

## 4. VRM / Power Delivery Components

### What the reports assume
- H100 SXM5: $165 (component harvesting for board-level repair)
- A100 SXM4: $85 (Vicor MCD + 2x MCM + 3x DC-DC)

### What actually exists

**VRM components are available as new parts from distributors.**

- Vicor MCM4608/MCM4609 current multiplier modules and MCD4609 driver modules are sold
  through authorized distributors (DigiKey, Allelco, TrustedParts). Pricing is not publicly
  listed but available on request.
- Vishay DrMOS (VRPower) power stages (SiC654, SiC780, SiC620R) are stocked at DigiKey and
  Mouser at $2-$8 per unit depending on current rating.
- MPS (Monolithic Power Systems) DrMOS stages used on H100 boards are also available through
  distribution.

**The salvage question is whether anyone buys *used, desoldered* VRM components.**

- The Shenzhen repair ecosystem does harvest VRM components from donor boards. Brother Zhang
  (Bilibili repair personality) documents this for custom GPU builds. Chinese shops source
  PCBs, use SMT lines to place VRM components, and build custom higher-VRAM cards.
- In the West, professional BGA rework services (Circuit Technology Center, BEST Inc.,
  Precision PCB Services) primarily work with new components, not harvested ones. Board-level
  repair shops may occasionally reuse a known-good inductor or MOSFET but this is not a
  systematic market.
- The practical issue: desoldering 61 power stages and 32 inductors from an H100 board
  requires hours of skilled labor. At Western labor rates ($50-$100/hr), the labor cost
  exceeds the component value.

### Realistic value

| Component | New price (distributor) | Harvested value |
|-----------|------------------------|-----------------|
| Vicor MCM4608/4609 module | ~$15-$30 (estimated, NDA pricing) | $5-$15 (if tested, Shenzhen market) |
| DrMOS power stage (50-70A) | $2-$8 new | $0.50-$2 harvested |
| Inductor (ferrite/Cu winding) | $0.50-$3 new | $0.10-$0.50 harvested |
| MLCC capacitor | $0.01-$0.10 new | Near $0 harvested |

The H100 VRM at $165 assumes all 61 power stages + 32 inductors + misc are harvested and
sold at near-new prices. Realistic recovery for the full VRM assembly:
- Shenzhen (skilled labor, existing demand): $30-$60
- Western market: $0-$15 (labor cost exceeds recovery)

**Report overstatement factor:** 3-10x depending on geography and labor economics.

Sources:
- [Vicor MCM4609 ChiP-set](https://www.vicorpower.com/press-room/2016-2021/hydra-ii)
- [DigiKey: Vicor distributor](https://www.digikey.com/en/supplier-centers/vicor)
- [Vishay VRPower DrMOS](https://www.vishay.com/en/power-ics/integrated-drmos/)
- [SemiAnalysis: AI power delivery competition](https://newsletter.semianalysis.com/p/energizing-ai-power-delivery-competition)

---

## 5. Coolers, Heatsinks, and Mechanical Components

### What the reports assume
- H100 SXM5 heatsink: $15 secondary market (generic Cu scrap), $21.69 raw scrap (1.8 kg Cu)
- PCIe card coolers: varies, $10-$30

### What actually exists

**This is the most straightforward salvage pathway.**

- Copper heatsinks are mechanically separable with no special equipment.
- Clean copper scrap (bare bright) trades at ~$5.90/lb ($13/kg) as of March 2026.
- A 1.8 kg copper heatsink from an H100 SXM5 module = ~$23 as clean Cu scrap.
- GPU cooler assemblies (fans + heatsink + backplate) from consumer cards sell on eBay as
  replacement parts: $20-$80 depending on card model and brand.
- Backplates, fan shrouds, and mounting hardware from popular cards (RTX 3090, RTX 4090)
  also sell individually on eBay for $10-$30.

### Realistic value

| Component | Realistic recovery |
|-----------|--------------------|
| SXM copper heatsink (1.8 kg) | $20-$25 (Cu scrap, no special effort) |
| PCIe card cooler assembly (popular model) | $20-$80 (eBay, if intact) |
| Backplate / shroud / fans separately | $10-$30 each (eBay) |
| Generic aluminum heatsink | $1-$3 (Al scrap) |

**Report accuracy: Reasonable.** The cooler/heatsink values in the reports are among the
most defensible numbers.

---

## 6. Connectors

### What the reports assume
- SXM5 mezzanine connector: $30 (replacement connector)
- SXM4 MEG-Array connectors: $30 total (2x$15)

### What actually exists

- SXM mezzanine connectors are specialty high-density components (Amphenol MEG-Array).
- They are available from electronic component distributors but are not commonly stocked
  in volume for aftermarket sale.
- The $30 figure is plausible for intact, desoldered connectors sold to the niche market of
  people building custom SXM-to-PCIe adapter projects (which do exist as hobbyist projects).
- Demand is extremely thin. These would sit unsold for months on eBay.

**Report accuracy: Plausible but illiquid.** Finding a buyer at $30 is possible but not
guaranteed.

---

## 7. Broken / Dead GPUs Sold Whole

### What actually happens in practice

The most common end-of-life pathway for a dead GPU is selling the whole card, not
parting it out. This is where real price data exists.

**Consumer GPUs (eBay "For Parts or Not Working"):**

| GPU Model | Working used price | "For parts" price | % of working |
|-----------|--------------------|-------------------|--------------|
| RTX 4090 | ~$2,200 | ~$200 (stripped, no die/VRAM) | ~9% |
| RTX 4090 | ~$2,200 | ~$400-$800 (dead but intact) | ~18-36% |
| RTX 3090 | ~$600-$800 | ~$100-$250 | ~15-35% |
| RTX 3080 | ~$350-$500 | ~$60-$150 | ~17-30% |
| Lot of 26 mixed dead GPUs | N/A | $226 total (~$8.70/card) | N/A |

**Datacenter GPUs:**

| GPU Model | Working used price | "For parts" price | Notes |
|-----------|--------------------|-------------------|-------|
| A100 40GB PCIe | ~$3,500-$4,500 | ~$1,500-$2,500 (memory errors) | Priced in bundle with working units |
| A100 SXM4 (untested baseboard, 8x) | ~$30,000-$50,000 | Listed but no sold data | Extremely niche |
| H100 (dead individual) | ~$9,600-$15,000 | No sold listings found | Market too new for dead units |

**Dedicated buyback services:**
- BrokenGPU.com buys broken NVIDIA and AMD cards in any condition. No specific price quotes
  are publicly listed; they use an instant-quote tool that updates weekly. Free shipping
  via USPS. Payment via PayPal or crypto.
- SellGPU.com buys used working components. Less clear on broken card acceptance.
- Net Equity buys used datacenter GPUs (A100, H100) for remarketing.

Sources:
- [BrokenGPU.com](https://www.brokengpu.com/)
- [SellGPU.com](https://sellgpu.com/)
- [Net Equity: NVIDIA GPU products](https://www.netequity.com/products/nvidia-gpu-products/)
- [ALTA Technologies: Used NVIDIA GPUs](https://altatechnologies.com/collections/used-nvidia-gpus)
- [TechSpot: Buyer of $1,600 RTX 4090 finds no GPU](https://www.techspot.com/news/101473-buyer-1600-second-hand-rtx-4090-finds-has.html)

---

## 8. Precious Metal Recovery (Gold, Silver, Palladium)

### What the reports assume
- H100 SXM5: ~$37 gross raw scrap (dominated by Cu heatsink at ~$22)
- Gold: ~$3.62 per H100 module (0.025g at $145/g)
- Consumer GPU: $22-$90 gold content (general estimates)

### What actually exists

**Professional precious metal recovery is a real industry but yields pennies per card.**

- Gold in a graphics card: 0.5-2g per card (general electronics industry estimates).
  However, the reports' own first-principles analysis found much less in SXM modules: ~0.02-0.03g
  (no PCIe gold edge fingers on SXM form factor).
- PCIe cards have more gold due to edge connector plating but still only ~0.1-0.5g.
- At March 2026 gold prices ($4,509/oz, $145/g), a PCIe GPU's gold content is worth $15-$72
  gross -- but professional refiners pay 40-60% of assay value after processing fees.
- Net payout per card from a precious metal refiner: $6-$43 (PCIe) or $1-$5 (SXM).
- Scrap PCBs (stripped of large components) trade at $0.50-$5.00/lb for consumer boards,
  $8-$20/lb for server-grade boards.
- E-waste recycling at scale: one ton of computer circuit boards yields ~$10,000 in gold
  (at >$2,000/oz gold), but you need roughly 300-500 GPUs to make one ton.

**The economics only work at industrial scale.** Sending 5-10 GPUs to a refiner is not
viable after shipping and minimum-lot fees.

Sources:
- [CJ Decycling: Circuit board gold recovery price guide](https://cjdecycling.com/circuit-board-gold-recovery-scrap-prices/)
- [Okon Recycling: Gold recovery from electronics](https://www.okonrecycling.com/consumer-recycling-initiatives/learn-about-recycling/gold-harvesting-electronics/)
- [iScrapApp: PC board scrap prices](https://iscrapapp.com/metals/pc-boards/)
- [BoardSort: Scrap circuit board payout](https://boardsort.com/payout.php)

---

## 9. GPU Repair Industry Overview

### Who actually repairs GPUs and what do they pay for dead cards?

**Western repair shops (US/EU):**
- NorthridgeFix (US), ZapFixers (US), NorthWest Repair (US): charge $199-$320+ for GPU
  repair. These shops buy dead cards on eBay/marketplace for $50-$200, attempt repair, and
  resell working cards at full used price. Their margin comes from the repair, not from
  component harvesting.
- Success rate is highly variable. Many "repairs" are simple firmware flashes, fan
  replacements, or reflows. True component-level repair (VRAM swap, MOSFET replacement) is
  rare and expensive.
- BGA rework equipment costs ~$100,000. Only a handful of Western repair shops have it.

**Shenzhen repair ecosystem (China):**
- ~12 firms servicing banned NVIDIA datacenter GPUs (A100, H100).
- Largest firm: 500 repairs/month. Pricing: $1,400-$2,800 per repair (~10% of retail).
- They DO harvest components from donor cards -- dies, VRM parts, connectors.
- The ecosystem includes custom PCB fabrication, SMT assembly lines, and component sourcing
  from Huaqiangbei market.
- Some shops build entirely custom GPUs (e.g., 48GB RTX 4090 variants) from harvested dies
  on third-party PCBs.

**Key insight:** The Western repair industry treats dead GPUs as repair candidates (buy
whole, fix, resell whole). The Shenzhen ecosystem treats dead GPUs as component donors
(harvest parts for other repairs or custom builds). The "component salvage" model in the
reports implicitly assumes the Shenzhen model, but that market is:
1. Geographically limited to China
2. Driven by sanctions-created artificial scarcity
3. Not accessible to Western datacenter operators decommissioning equipment

Sources:
- [NorthridgeFix](https://northridgefix.com/)
- [ZapFixers: GPU repair service](https://zapfixers.com/services/gpu-repair/)
- [Tom's Hardware: Underground China repair shops](https://www.tomshardware.com/pc-components/gpus/underground-china-repair-shops-thrive-servicing-illicit-nvidia-gpus-banned-by-export-restrictions-companies-resurrecting-banned-ai-accelerators-at-a-rate-of-up-to-500-per-month)
- [NotebookCheck: Gray-market repairs in China](https://www.notebookcheck.net/Gray-market-repairs-for-banned-Nvidia-H100-and-A100-GPUs-surge-in-China.1069609.0.html)

---

## 10. Summary: Is "Component Salvage" a Real Recovery Path?

### Verdict: Mostly theoretical. Real for a few parts, in a few places.

| Component | Liquid market exists? | Realistic recovery | Report accuracy |
|-----------|----------------------|--------------------|-----------------|
| GPU die (bare) | No (Shenzhen gray market only) | $0 (West), $200-$800 (Shenzhen, datacenter dies only) | 3-200x overstated |
| HBM stacks | No | $0 | Completely fictional value |
| GDDR6/6X VRAM chips | Yes (AliExpress, repair shops) | $3-$20/chip new, $1-$5 harvested | Reasonable if broken out |
| VRM power stages | Marginal (new parts available; harvested market thin) | $30-$60 (Shenzhen), $0-$15 (West) | 3-10x overstated |
| Cooler/heatsink | Yes (eBay, Cu scrap) | $20-$80 (consumer), $20-$25 (SXM Cu scrap) | Accurate |
| Connectors | Barely (niche hobbyist) | $10-$30 (if buyer found) | Plausible but illiquid |
| PCB (bare) | Yes (e-waste recyclers) | $0.50-$5/lb | Accurate |
| Precious metals | Yes (industrial refiners, at scale only) | $6-$43 net per PCIe card, $1-$5 per SXM module | Accurate |
| Whole dead card | Yes (eBay, BrokenGPU.com, repair shops) | 15-35% of working used price | N/A (not in reports) |

### What the reports should say

The "component salvage" line in each report is presented as a single number (e.g., $2,310
for H100 SXM5, $630 for A100 SXM4) that implies recoverable value. In reality:

1. **The only universally accessible salvage value is selling the dead card whole.** A dead
   H100 would likely sell for $1,000-$3,000 to a specialized broker (Net Equity, ALTA
   Technologies) or on eBay. A dead A100 might fetch $500-$1,500. These are real,
   observable transactions.

2. **Component-level harvesting only makes economic sense in Shenzhen**, where labor is
   cheap, demand is artificially elevated by sanctions, and the supporting infrastructure
   (BGA rework, custom PCB fab, Huaqiangbei component market) exists within a few square
   kilometers. This is not a generalizable recovery pathway.

3. **HBM stack values are pure fiction.** No one buys individual HBM stacks. They cannot be
   removed from CoWoS packages without destroying them (or at minimum, without TSMC-class
   equipment that no repair shop possesses). The $1,200 figure for H100 HBM should be $0.

4. **The most defensible component salvage items are: coolers, fans, backplates, and
   individual VRAM chips** (for consumer cards only). These have real eBay/AliExpress
   markets with observable prices.

5. **For datacenter end-of-life planning, the correct salvage assumption is: sell the whole
   card to a broker or remarketing firm.** Component-level teardown is not economically
   rational at Western labor rates.

### Recommended revision to reports

Replace the single "component salvage" line with two lines:

| Scenario | H100 SXM5 example | A100 SXM4 example |
|----------|-------------------|-------------------|
| Dead card sold whole (broker/eBay) | $1,000-$3,000 | $500-$1,500 |
| Component teardown (Shenzhen only, theoretical) | $800-$1,500 | $200-$400 |
| Component teardown (Western, net of labor) | $20-$80 (heatsink + PCB scrap only) | $10-$30 |

---

## Sources

### Stripped/Harvested GPU Market
- [Tom's Hardware: Stripped RTX 4090 from eBay](https://www.tomshardware.com/pc-components/gpus/used-rtx-4090-from-ebay-shows-up-with-no-gpu-chip-or-video-memory-stripped-asus-tuf-rtx-4090-points-to-increasing-number-of-scams-in-the-used-gpu-market)
- [Tom's Hardware: RTX 4090 returned with GPU/VRAM removed](https://www.tomshardware.com/pc-components/gpus/pristine-rtx-4090-returned-to-ebay-seller-with-gpu-and-vram-chips-missing)
- [TechSpot: $1,600 RTX 4090 with no GPU](https://www.techspot.com/news/101473-buyer-1600-second-hand-rtx-4090-finds-has.html)
- [TechRadar: Broken/GPU-less RTX 4090s sold by scammers](https://www.techradar.com/computing/gpu/broken-and-gpu-less-rtx-4090s-are-being-sold-secondhand-by-scammers)
- [Tom's Hardware: Fake 4090s from 30-series chips](https://www.tomshardware.com/pc-components/gpus/customer-sends-four-rtx-4090s-to-a-repair-technician-finds-out-three-are-fake-new-counterfeiting-technique-uses-modded-30-series-chips)

### Shenzhen Gray Market
- [Tom's Hardware: Underground China repair shops (500/month)](https://www.tomshardware.com/pc-components/gpus/underground-china-repair-shops-thrive-servicing-illicit-nvidia-gpus-banned-by-export-restrictions-companies-resurrecting-banned-ai-accelerators-at-a-rate-of-up-to-500-per-month)
- [NotebookCheck: Gray-market repairs for banned GPUs](https://www.notebookcheck.net/Gray-market-repairs-for-banned-Nvidia-H100-and-A100-GPUs-surge-in-China.1069609.0.html)
- [TechRadar: China surge in unauthorized AI chip repairs](https://www.techradar.com/pro/potentially-tens-of-thousands-of-faulty-nvidia-ai-chips-end-up-in-these-obscure-chinese-repair-shops-it-may-mask-something-even-more-vital)
- [GamersNexus: NVIDIA AI GPU Black Market](https://gamersnexus.net/gpus-deep-dive-news/nvidia-ai-gpu-black-market-investigating-smuggling-corruption-governments)
- [Shenzhen Shops Repair Smuggled Nvidia AI Chips](https://www.webpronews.com/shenzhen-shops-repair-smuggled-nvidia-ai-chips-defying-us-bans/)

### GPU Repair Services
- [NorthridgeFix](https://northridgefix.com/)
- [ZapFixers: GPU repair](https://zapfixers.com/services/gpu-repair/)
- [Overclock.net: Best GPU repair in US](https://www.overclock.net/threads/best-graphics-card-repair-business-in-the-united-states.1809284/)
- [Tom's Hardware: GPU reballing service pricing](https://forums.tomshardware.com/threads/graphics-video-card-reballing-repair.3258254/)
- [Overclockers Forums: Cost of GPU repair](https://www.overclockers.com/forums/threads/cost-of-gpu-repair.804179/)

### BGA Rework Industry
- [Circuit Technology Center: BGA rework](https://www.circuitrework.com/services/bga-rework.html)
- [BEST Inc: BGA rework services](https://www.solder.net/services/bga-rework-services/)
- [Precision PCB Services: BGA rework](https://precision-pcb-services-inc.com/products/bga-rework-service)
- [STI Electronics: BGA rework](https://stiusa.com/rework-repair/)

### Component Markets
- [AliExpress: GDDR6X memory chips](https://www.aliexpress.com/w/wholesale-gddr6x-memory-chip.html)
- [DigiKey: Vicor distributor](https://www.digikey.com/en/supplier-centers/vicor)
- [Vishay: VRPower DrMOS](https://www.vishay.com/en/power-ics/integrated-drmos/)
- [Allelco: Vicor MCD4609](https://www.allelcoelec.com/productdetails/Vicor/mcd4609s60e59h0t20.html)

### Broken GPU Market
- [BrokenGPU.com](https://www.brokengpu.com/)
- [SellGPU.com](https://sellgpu.com/)
- [Net Equity: NVIDIA GPU products](https://www.netequity.com/products/nvidia-gpu-products/)
- [ALTA Technologies: Used NVIDIA GPUs](https://altatechnologies.com/collections/used-nvidia-gpus)

### Scrap / Precious Metal Recovery
- [CJ Decycling: Circuit board gold recovery price guide](https://cjdecycling.com/circuit-board-gold-recovery-scrap-prices/)
- [Okon Recycling: Component salvage](https://www.okonrecycling.com/consumer-recycling-initiatives/learn-about-recycling/component-salvage/)
- [Okon Recycling: Electronics parts harvesting](https://www.okonrecycling.com/consumer-recycling-initiatives/learn-about-recycling/electronics-parts-harvesting/)
- [iScrapApp: PC board scrap prices](https://iscrapapp.com/metals/pc-boards/)
- [BoardSort: Scrap circuit board payout](https://boardsort.com/payout.php)
- [Infinity Turbine: Precious metals in H100](https://infinityturbine.com/gold-recovery-from-nvidia-h100-gpu-co2-extraction-by-infinity-turbine.html)
- [Tom's Hardware: GDDR6 VRAM prices](https://www.tomshardware.com/news/gddr6-vram-prices-plummet)

### HBM Market
- [Wikipedia: High Bandwidth Memory](https://en.wikipedia.org/wiki/High_Bandwidth_Memory)
- [Micron: HBM3E](https://www.micron.com/products/memory/hbm/hbm3e)
- [Tom's Hardware: What is HBM](https://www.tomshardware.com/reviews/glossary-hbm-hbm2-high-bandwidth-memory-definition,5889.html)
