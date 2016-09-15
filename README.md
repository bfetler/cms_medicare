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
+ payment per service = log10 ( total Medicare payment amount / total number of services )
+ payment per person = log10 ( total Medicare payment amount / total number of beneficiaries )

We find a log scale gives data closer to a normal distribution, and use log base 10 for numerical convenience.  Grouping the payments by the 91 provider types in the data, we find a lot of variation for each provider type.  Histograms for all provider types are given in __cms_hist_plots/__.  A histogram of some specialties is shown below.  

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_hist_plots/hist_pay_per_person_group7.png" alt="example histogram per person" />

A good number of provider types have well-defined costs that follow a log normal distribution, while others have a lot of variation.  Some categories have very few providers, for whom it is difficult to do statistics.  Nonetheless, we find some trends by provider type.

#### Payment Per Service
Of the top dozen provider types by median payment per service, nine are for Surgery, with the most expensive being Ambulatory Surgery, and three are for Radiation or Oncology.  A summary is given in the table and figure below.  

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

#### Medicare Total Beneficiaries and Payment

The total number of medicare beneficiaries by provider type is shown below.  This gives some idea of the most and least popular care options provided by Medicare.  Diagnostic Radiology, Internal Medicine, Clinical Laboratory and Cardiology are in the top five most popular.

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_pop_plots/bar_total_unique_benes_sum.png" alt="bar plot total beneficiaries" />

The total medicare payment by provider type is shown below.  This gives some idea of the most and least expensive care provided by Medicare.  Internal Medicine, Ophthalmology, Clinical Laboratory and Cardiology are in the top five most expensive.

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_pop_plots/bar_total_medicare_payment_amt.png" alt="bar plot total payment" />

#### Medicare Payment By State

Absolute cost per service of each provider type is shown above in the figure "Median Log10 Pay Per Person".

To show relative cost, maps of median cost per service by state were created for provider types.  Three common provider types are shown in the figures below:
+ General Surgery (expensive)
+ Internal Medicine (intermediate cost)
+ Physical Therapist (inexpensive)

A median color of red was used for each map, with more expensive states trending purple and less expensive states trending yellow.

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_state_person_plots/map_cost_per_person_general_surgery.png" alt="median cost per person by state for general surgery" />

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_state_person_plots/map_cost_per_person_internal_medicine.png" alt="median cost per person by state for internal medicine" />

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_state_person_plots/map_cost_per_person_physical_therapist.png" alt="median cost per person by state for physical therapist" />

Some of the western states such as Utah and Montana appear to be more expensive for some surgeries, while the northeast and Florida are moderately expensive.

#### Provider Gender

We further analyzed the data by provider gender, with some types of facilities categorized as neither.  In general, we find some specialties have a sizeable gender gap, while others do not.  This somewhat reflects traditional roles in society, with more female nurses and more male surgeons.  

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_gender_plots/bar_count_fraction.png" alt="gender count bar plot" />

We also find that female providers generally cost less than male providers, depending on specialty.  Consumers who choose female providers may see reduced costs.  On the other hand, the data also may indicate a persistent wage gap among female providers.  The median cost ratio is less than 20% for 80% of providers.  

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_gender_plots/bar_cost_ratio.png" alt="gender cost ratio bar plot" />

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_gender_plots/scatter_cost_ratio_by_fraction.png" alt="gender cost ratio scatter plot" />

Here is an example plot of a histogram of log costs by provider gender.  There does not appear to be a large difference in cost distribution based upon gender for most provider types.

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_hist_gender_plots/hist_gender_pay_per_person_group7.png" alt="gender cost histogram plot" />

#### Patient Age

We have data on average patient age, and age broken into four categories, which we can group by provider type.  The information is not broken down into cost per service by age, but it is still interesting to consider the popularity of different specialists by age.  

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_pop_plots/bar_beneficiary_average_age.png" alt="beneficiary average age by provider" />

Apparently Psychiatry is needed more by people in their mid-50's, while Radiation Oncology is more common in the mid-70's.  

<img src="https://github.com/bfetler/cms_medicare/blob/master/bene_average_age_plots/hist_beneficiary_average_age_group7.png" alt="beneficiary age subgroup" />

#### Patient Gender

Patient gender also affects the types of medical procedures needed.  The results are for total population.  

<img src="https://github.com/bfetler/cms_medicare/blob/master/cms_pop_gender_plots/bar_provider_type_group1.png" alt="beneficiary gender subgroup" />

#### Conclusion

Health care costs are a sobering reminder for consumers and anyone concerned with health care in the U.S.
