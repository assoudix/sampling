https://www.millercanfield.com/resources-May-Taxpayer-Rely-on-Statistical-Sampling-to-Calculate-Research-Tax-Credits.html
https://www.thetaxadviser.com/issues/2022/feb/research-credit-using-statistical-sampling.html
https://www.irs.gov/businesses/audit-techniques-guide-credit-for-increasing-research-activities-ie-research-tax-credit-sampling-methodologies
https://www.irs.gov/pub/irs-lbi/field_directive_samp_method_research_credit_cases.pdf
https://www.coursera.org/learn/sampling-methods
_____________________________________________________
DIY Stratified Statistical Sampling for R&D Tax Credit
1. Create Your Population Database
•	List all projects in a spreadsheet with columns for: 
o	Project ID/name
o	Total project cost
o	Stratum (packaging, food, pharma, maritime, etc.)
o	Any other relevant classification data

>> integrated pull functionality from python lists as well

2. Determine Sample Sizes (to be integrated)
For each stratum:
•	If fewer than 50 projects, consider examining all of them
•	Otherwise, a sample size of 30-50 is typically sufficient
•	Use this formula for more precision: n = (z²σ²N)/((N-1)e² + z²σ²) 
o	n = sample size
o	z = confidence level (1.96 for 95% confidence)
o	σ = standard deviation (estimate if unknown)
o	N = population size
o	e = margin of error (typically 0.05 or 5%)

3. Generate Random Samples
implemented using a Python script
4. Automate documentation (TBD)


License: MIT
