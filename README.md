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
+ summary of anonymized beneficiary information

### Preliminary Analysis
To get an idea of actual health care costs for consumers, we did a preliminary analysis of the total Medicare payment amount per service and per beneficiary.  Typically, a beneficiary has supplemental insurance to cover the remainder of the claims, which often pays 20% of the approved Medicare payment.  Extra costs are typically fixed at a fraction of the approved payment.  We calculated two extra columns:
+ payment per service = total Medicare payment amount / total number of services
+ payment per person = total Medicare payment amount / total number of beneficiaries

Grouping the payments by the 91 provider types in the data, we find some trends.  

##### Payment Per Service
Of the top twenty provider types by median payment per service, eleven are for Surgery, with the most expensive being Ambulatory Surgery, and three are for Oncology or Radiation.  They are given in the table below.  

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
<tr><td>Critical Care</td><td>117</td></tr>
<tr><td>CRNA</td><td>115</td></tr>
<tr><td>Anesthesiologist Assistants</td><td>109</td></tr>
<tr><td>Maxillofacial Surgery</td><td>105</td></tr>
<tr><td>Independent Diagnostic Testing Facility</td><td>105</td></tr>
<tr><td>Oral Surgery (dentists only)</td><td>100</td></tr>
<tr><td>Gastroenterology</td><td>98</td></tr>
<tr><td>Ophthalmology</td><td>90</td></tr>
</table>

##### Payment Per Beneficiary
Of the top twenty provider types by median payment per beneficiary, five are for Oncology or Radiation, with the most expensive being Radiation Therapy, and six are for Surgery, as given in the table below.  

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
<tr><td>Hematology/Oncology</td><td>453</td></tr>
<tr><td>Occupational therapist</td><td>448</td></tr>
<tr><td>Interventional Pain Management</td><td>437</td></tr>
<tr><td>Licensed Clinical Social Worker</td><td>418</td></tr>
<tr><td>Surgical Oncology</td><td>407</td></tr>
<tr><td>Nephrology</td><td>397</td></tr>
<tr><td>Gynecological/Oncology</td><td>386</td></tr>
<tr><td>Colorectal Surgery</td><td>380</td></tr>
</table>

For consumers, the payment per person is probably of most interest, since one is typically prescribed a series of treatments.

There is a lot of variation in the data for each provider type.  Some have well-defined costs with little variation, while others have widely varying distributions.  Others have very few providers, for whom it is difficult to do statistics.  For example:
+ The standard error is greater than the mean or median for *Payment Per Person* for Radiation Oncology, Ambulance Service Supplier, Cardiology, Clinical Laboratory, Hematology, Medical Oncology, Nuclear Medicine and Vascular Surgery.  
+ The standard error is greater than the mean or median for *Payment Per Service* for Ambulance Service Supplier, Clinical Laboratory, Hematology/Oncology, Nuclear Medicine, Oral Surgery and Urology.  
+ There are 51 Radiation Therapy providers, while there are 4363 Radiation Oncology providers.  There is only 1 Interventional Cardiologist.  

The variation in costs may be due to the type of facility (e.g. major hospital or not) or location (e.g. urban or rural area), and requires further investigation.  

The costs are a sobering reminder for consumers and anyone concerned with health care costs in the U.S.
