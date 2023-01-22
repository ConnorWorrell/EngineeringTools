### Calculators

#### Plan

- [ ] Bolt thread calculator
    - [ ] Convert standard ASME B1.3-2007 to thread profile
    - [ ] Convert ISO threads to ISO 68-1 and ISO 262
    - [ ] Report: Pitch, diameters, root radius, tolerances
    - [ ] Predict or record cut threads vs rolled threads
    - [ ] Input material/suggest commonly avalible materials for COTS materials

- [ ] Bolted Joint calculator
    Report Safety Factor of bolted joints in various environments
    - [ ] Core
        - [ ] Input thread profiles from Bolt thread calculator
        - [ ] Input various thread configurations: Through bolt+nut, stud, tapped bolt.
        - [ ] Input various clamping materials, N layers with any thickness, friction.
        - [ ] Predict contact pressure
            - [ ] Input plate sizes
            - [ ] Report expected contact pressure area/profile
        - [ ] Evaluate static strength
        - [ ] Evaluate fatigue
            - [ ] Input fatigue parameters
        - [ ] Predict fasener torque/tightening process
            - [ ] Input tightening process
        - [ ] Thermal effects
            - [ ] Input temperature ranges of joint
            - [ ] Evaluate relaxation/tightening from CTE
        - [ ] Loosening
            - [ ] Input local strain to evaluate slip
            - [ ] Embedment/surface finish
            - [ ] Creep
            - [ ] Locknuts/washers/patches
        - [ ] Accurately predict effects of corrosion
            - [ ] Environmental factors
        - [ ] Report
            - [ ] Clamping spread
            - [ ] Tightening torque
            - [ ] Fatigue life
            - [ ] Time between inspections
                - Preload loss
                - Clamping spread over time
    - [ ] GUI

- [ ] Corrosion Calculator
    - Accurately predict corrision in many senarios
