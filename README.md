## Center for Medicare Services Data

The Center for Medicare Services (CMS) has provided public datasets for many different aspects of healthcare, in an attempt to make the U.S. healthcare system more transparent.  The most recent healthcare provider data from 2014 is available in the [Medicare Provider Utilization and Payment Data: Physician and Other Supplier Public Use File](https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Physician-and-Other-Supplier2014.html).  

The file contains annual data from over 980,000 physicians and other healthcare providers, including: 
+ provider type
+ provider location
+ total cost of submitted claims
+ total Medicare payment amount 
+ total number of services (doctors visits or procedures)
+ total number of beneficiaries (patients)
+ some drug costs (full drug data is in other datasets)
+ provider and patient gender
+ summary of anonymized beneficiary information

### Preliminary Analysis
To get an idea of actual health care costs for consumers, we did a preliminary analysis of the total Medicare payment amount per service and per beneficiary.  Typically, a beneficiary has supplemental insurance to cover the remainder of the claims, which often pays 20% of the approved Medicare payment.  Extra costs are typically fixed at a fraction of the approved payment.  We calculated two extra columns:
+ payment per service = total Medicare payment amount / total number of services
+ payment per person = total Medicare payment amount / total number of beneficiaries

Grouping the payments by the 91 provider types in the data, we find a lot of variation for each provider type.  Histograms for all provider types are given in __cms_hist_plots/__.  A histogram of some specialties is shown below.  

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_hist_plots/hist_pay_per_person_group7.png" alt="example histogram per person" />

A good number of provider types have well-defined costs that follow a normal distribution on a log scale, while others have a lot of variation.  Some categories have very few providers, for whom it is difficult to do statistics.  The variation in costs may be due to the type of facility (e.g. major hospital or not) or location (e.g. urban or rural area), and requires further investigation.  

We find some trends by provider type.

#### Payment Per Service
Of the top dozen provider types by median payment per service, nine are for Surgery, with the most expensive being Ambulatory Surgery, and three are for Radiation or Oncology.  A sorted, ranked summary is given in the table and figure below.  

<table>
<th>Provider Type</th><th>Payment Per Service (USD)</th>
<tr><td>Ambulatory Surgical Center</td><td>457</td></tr>
<tr><td>Cardiac Surgery</td><td>353</td></tr>
<tr><td>Thoracic Surgery</td><td>262</td></tr>
<tr><td>Neurosurgery</td><td>220</td></tr>
<tr><td>Surgical Oncology</td><td>167</td></tr>
<tr><td>Plastic and Reconstructive Surgery</td><td>164</td></tr>
<tr><td>Radiation Therapy</td><td>155</td></tr>
<tr><td>Colorectal Surgery</td><td>152</td></tr>
<tr><td>General Surgery</td><td>145</td></tr>
<tr><td>Anesthesiology</td><td>131</td></tr>
<tr><td>Vascular Surgery</td><td>125</td></tr>
<tr><td>Gynecological/Oncology</td><td>118</td></tr>
</table>

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_cost_plots/bar_pay_per_service.png" alt="bar plot per service" />

#### Payment Per Beneficiary
Of the top dozen provider types by median payment per beneficiary, two are for Radiation or Oncology, with the most expensive being Radiation Therapy, and five are for Surgery, as shown in the table and figure below.  

<table>
<th>Provider Type</th><th>Payment Per Person (USD)</th>
<tr><td>Radiation Therapy</td><td>7039</td></tr>
<tr><td>Cardiac Surgery</td><td>934</td></tr>
<tr><td>Ambulatory Surgical Center</td><td>893</td></tr>
<tr><td>Psychologist (billing independently)</td><td>867</td></tr>
<tr><td>Radiation Oncology</td><td>830</td></tr>
<tr><td>Thoracic Surgery</td><td>689</td></tr>
<tr><td>Ambulance Service Supplier</td><td>580</td></tr>
<tr><td>Clinical Psychologist</td><td>571</td></tr>
<tr><td>Neurosurgery</td><td>549</td></tr>
<tr><td>Physical Therapist</td><td>529</td></tr>
<tr><td>Plastic and Reconstructive Surgery</td><td>500</td></tr>
<tr><td>Speech Language Pathologist</td><td>463</td></tr>
</table>

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_cost_plots/bar_pay_per_person.png" alt="bar plot per person" />

For consumers, the payment per person is probably of most interest, since a patient is typically prescribed a series of treatments, not just a single service.

#### Provider Gender

We further analyzed the data by provider gender, with some types of facilities categorized as neither.  In general, we find some specialties have a sizeable gender gap, while others do not.  This somewhat reflects traditional roles in society, with more female nurses and more male surgeons.  

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_gender_plots/bar_count_fraction.png" alt="gender count bar plot" />

We also find that female providers generally cost less than male providers, depending on specialty.  Consumers who choose female providers may see reduced costs.  On the other hand, the data also may indicate a persistent wage gap among female providers.  The median cost ratio is less than 20% for 80% of providers.  

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_gender_plots/bar_cost_ratio.png" alt="gender cost ratio bar plot" />

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_gender_plots/scatter_cost_ratio_by_fraction.png" alt="gender cost ratio scatter plot" />

Here is an example plot of a histogram of log costs by provider gender.  There does not appear to be a large difference in cost distribution based upon gender *(red=female, green=male, blue=facility)* for most provider types.

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_hist_gender_plots/hist_gender_pay_per_person_group7.png" alt="gender cost histogram plot" />

#### Conclusion

The costs are a sobering reminder for consumers and anyone concerned with health care costs in the U.S.
