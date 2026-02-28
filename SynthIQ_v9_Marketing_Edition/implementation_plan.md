# Behavioral Drift Engine UI Implementation Plan

This plan details the creation of a premium, interactive dashboard for the Behavioral Drift Engine, mimicking the "SynthIQ" aesthetic.

## Proposed Changes

# SynthIQ Master Platform UI Implementation Plan

This plan details the creation of the **SynthIQ Enterprise Dashboard**, a comprehensive platform integrating Persona Intelligence, A/B Testing, and Behavioral Drift analysis as outlined in the SAP AI Persona document.

## Proposed Changes

### [Component] SynthIQ Master Platform (SPA)
Create a premium, multi-module dashboard using HTML, CSS, and JS.

#### [NEW] [synthiq-master-platform.html](file:///C:/Users/sandh/OneDrive/GLIM%20PGDM%20-1/Term%203/SAP%20HACKFEST/synthiq-master-platform.html)
- **Module 1: Dashboard Overview**: High-level KPIs (Total Personas, Simulation Confidence, Market Volatility).
- **Module 2: Persona Vault**: 
    - Display the 10 data-grounded personas.
    - Deep-dive profiles with clustering stats (KMeans centroids).
- **Module 3: Campaign Lab (A/B Testing)**: 
    - Input fields for Product A (Description/Price) and Product B.
    - "Run Simulation" button that triggers LLM-style evaluation logic (simulated in JS).
    - Resulting Comparison: Conversion Uplift, ROAS estimates.
- **Module 4: Behavioral Drift Engine**: 
    - Port the existing Drift Lab v2 into a dedicated tab.
    - Stress-test the "Winning" variant from Module 3 against future macro/personal shocks.
- **Module 5: Project Finance**: 
    - ROI calculator, CAC/CLTV projections, and Market TAM/SAM/SOM charts.

## Implementation Strategy
### [Component] Dynamic Strategy Evaluation Engine
Eliminate hardcoded bias by implementing a text-resonance engine that calculates winners based on actual campaign keywords vs. audience sensitivity.

#### [MODIFY] [synthiq-master-platform.html](file:///C:/Users/sandh/OneDrive/GLIM%20PGDM%20-1/Term%203/SAP%20HACKFEST/synthiq-master-platform.html)
- **Keyword Resonance Matrix**:
    - *Economic/Value Keywords*: "Daily", "Micro", "₹19", "Cheap", "Access", "Affordable".
    - *Premium/Status Keywords*: "Premium", "₹499", "Luxury", "Status", "Subscription".
- **Dynamic Winning Logic**:
    - The engine will scan `desc-a` and `desc-b` for these keywords.
    - Since 60%+ of the population is currently "Value-Oriented" (Dailyists, Savers, Climbers), a campaign with more *Economic* keywords will gain higher resonance.
    - If the user interchanges the text, the winner will pivot accordingly.
- **Dynamic Rationale**:
    - The simulation rationale will mention specific keywords found in the text (e.g., *"The 'Micro-Pay' model resonated with 82% of the Budget Cautious segment"*).

### Manual Verification
1. Launch `synthiq-master-platform.html`.
2. Navigate to **Persona Vault** and verify 10 profiles are listed.
3. Use **Campaign Lab** to simulate an A/B test and check the "Victory Recommendation".
4. Navigate to **Behavioral Drift** to see how the winner holds up under a 10% inflation spike.
5. Verify **Project Finance** tab displays the breakeven analysis.

## Porting Strategy
The Python logic will be translated to Javascript:
- **Macro Sensitivity**: `coeffs.alpha`, `coeffs.beta`, `coeffs.gamma` per cluster.
- **Randomization**: `Math.random()` to trigger personal micro-shocks on each "instance".
- **Sigmoid**: Standard $1 / (1 + e^{-k(x-x0)})$ implementation.

## Verification Plan

### Manual Verification
1. Open `drift-engine-dashboard.html` in a browser.
2. Adjust inflation and rates; verify that the persona cards update dynamically.
3. Trigger a "Price Hike" and observe the spending propensity erosion.
4. Verify that the "Personal Shocks" log shows unique events (e.g., "Career Setback", "Family Transition") for different samples.
