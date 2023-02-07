# Comments on NIST SP 800-216

https://csrc.nist.gov/publications/detail/sp/800-216/draft

https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-216-draft.pdf

Public comment period: June 7, 2021 through August 9, 2021

Email: sp800-216-comments@nist.gov

Please put the section name and line numbers when quoting text.

# General comments

The language in this draft is not clear, e.g. is SHOULD/MUST being used in accordance with RFC2119?

The draft appears to focus exclusively on traditional software products run by end users and appears to ignore cloud services and other newer technologies and delivery methods.

# Specific comments below

Section: 234 1. U.S. Government Vulnerability Disclosure

```
235 Thousands of security vulnerabilities in computer software and systems are discovered and
236 publicly disclosed every year. Likely, even more are discovered by developers and quietly fixed
```
Thousands is on the low end, there are ~16000 CVEs assigned yearly (by CVE Identifier YEAR, for the last 4 years. For example a quick search of GitHub shows hundreds of thousands: https://github.com/search?q=%22security+fix%22 and this ignores the cloud services, and non english speaking world largely.

```
237 without anyone ever being aware. In 2020 alone, there were over 18,000 publicly listed
```

This number is unclear. By Assigned data and by YEAR in the CVE ID:

```
curl https://cve.mitre.org/data/downloads/allitems.csv | grep -a "^CVE-2020-" | grep -v "\* RESERVED \*" | wc -l
17802

curl https://cve.mitre.org/data/downloads/allitems.csv | grep -a "Assigned (2020[0-9][0-9][0-9][0-9]" | grep -v "\* RESERVED \*" | wc -l
17000
```

The git repo may have different data but walking all the files to extract the time they actually went public with data needs to be done at some point.

Section: 334 1.1. Usage of Document Terminology

```
335 In the context of this document, the term “vulnerability” refers to a security vulnerability in a
336 digital product. It does not refer to other kinds of vulnerabilities that may pertain to, for example,
337 physical security, economic security, or foreign policy issues.
```

Assuming digital products includes cloud services then physical security is a valid concern. Please note that the word "cloud" only occurs once in the document in a reference to ISO IEC 27017. This creates a significant blindspot as 1) many government agencuies use cloud services and 2) many software and "digital products" make use of cloud services (licensing management, updates, data storage and processing, etc.). 

Section: 396 2.1.1. Create Vulnerability Report Receipt Capability

```
397 Each FCB participant should develop the ability to receive vulnerability reports from reporters,
398 maintain a database of received reports, and engage in secure communications (e.g., using a
399 report tracking system). The expectation for communication should be established, including the
400 initial acknowledgment, status updates, and agreed method of communication. The actual receipt
401 of a vulnerability report may take multiple forms (e.g., email, web forms, or a phone hotline) and
402 should be stated in a public policy
```

Where will these policies be published, and how will people find them? There are no generally accepted standards here, e.g. do they use domain.tld/security/ or domain.tld/.well-known/security.txt (https://securitytxt.org/) or simply rely on al ink in the front page or the "contact us" page? Discovery of how to report an issue is problematic and can result in people giving up and not reporting issues, or extra time being required during an emergency to find out whom to contact and how to contact them.

```
408 Vulnerability reports should include a description of the product or service affected; how the
409 potential vulnerability can be identified, demonstrated, or reproduced; and what type of
410 functional impact the vulnerability allows. Due to the sensitivity of the information, agencies
411 should provide mechanisms for confidentially receiving additional information within the reports
412 (e.g., web forms, bug or issue tracking systems, vulnerability reporting services, email, or role
413 address independent of any individual). To facilitate verification of the vulnerability, agencies
414 should design the reporting mechanisms that lead to better information in assessing the validity,
415 severity, scope, and impact of vulnerabilities. This information could include:
```

No mention is made of reporting formats or standards, e.g. CVE JSON format? CSAF? OSV? UVI?

Section: 429 2.1.2. Determine Scope and Obtain Contacts

```
430 Prior to the receipt of any vulnerabilities, each FCB participant will determine which government
431 VDPOs fall within the scope of their services. The FCB entity will then obtain and maintain a list
432 of VDPO contacts within the relevant government agencies that receive and handle vulnerability
```

This appears to assume a traditional top down pyramid structure, is there any thought giving to lateral reporting or more of a matrix style layout to allow multiple pathways? Top-down reporting strucutres tend to suffer from the fact they are entirely comprised of a chain of single paths of failure.

Section: 516 2.7.1. Determination of Public Disclosure

```
521 Public disclosure may be considered if:
522 • The specific vulnerability is not publicly known (i.e., does not have a CVE number);
```

It is not clear if this advice implies that a CVE identifier should be obtained or not. 

```
531 In many cases, public disclosure might not be necessary or even recommended. For example,
532 publication is likely unnecessary if the vulnerable system is a service that government staff have
533 fixed and they can verify that the vulnerability was not exploited. Vulnerabilities that have been
534 fixed and had no impact on the system userbase should likely not be publicly disclosed in order
535 to enable the advisory systems to focus on vulnerabilities that require user action for continued
536 security and privacy.
```

This may create an incentive to cover security vulnerabilities up with a "we fixed it and we're pretty sure nobody exploited it" creating a false sense of security for end users. I would suggest it is better to report incidents, even onces that have been fully handled and pose no significant risk, and 1) label them as such "no action required" and 2) it allows for the creation of actual data and statistics, e.g. a system has 100 security vulnerabilities that were closed out before they became a problem, is this an indication of a security team that is really on the ball, or a team that is covering up real vulnerabilities as "not a problem" and so on? Without any data and reporting there is a strong possibility for institutional rot to set in.

Section: 627 2.7.3.2. National Vulnerability Database

```
628 The National Vulnerability Database [NVD] is the U.S. Government repository of standards-
629 based vulnerability management data. It contains a database of almost all publicly disclosed
630 vulnerabilities — more specifically, all vulnerabilities included within the Common
631 Vulnerabilities and Exposures (CVE) dictionary [CVE]. NVD staff analyzes vulnerability
```

The CVE database is missing a huge amount of content:

1) CVEs that have been assigned, but the data not pushed back to the database (some of which is over 10 years old): https://github.com/distributedweaknessfiling/distributedweaknessfiling.org/tree/main/reserved-but-public
2) Many CNAs have security vulnerabilities and advisories with no CVE IDs, e.g. XEN (goto https://xenbits.xen.org/xsa/ and look for "none (yet) assigned")
3) Non CNA data sources with in scope content
4) Non CNA sources with "out of scope" but useful data (e.g. services, malware, backdoors, etc.)

Section: 683 2.9. Technical Approaches and Resources

```
689 The CVE naming scheme should be used when referencing publicly disclosed vulnerabilities.
690 The CVE website is focused on providing unique identification for each vulnerability to maintain
691 the CVE list. It is not intended to act as an advisory service. When referencing a CVE
692 vulnerability, the NVD link should be used since it provides an analysis of each CVE and any
693 referenced information.
```

This will require the CVE system to be much more responsive and cover a much wider scope of vulnerabilities. It's also not clear on what will happen if a CNA refuses to create CVE identifiers, I can only assume the CVE dispute process will be invoked. The reality is the US Government uses a LOT of OpenSource software for which there is poor, if any, CVE coverage currently. 


Section: 794 3.2.2. Monitoring of Vulnerability Reports

```
795 VDPOs should monitor their reporting mechanisms for new reports and communications related
796 to existing reports. VDPOs should also monitor public sources for vulnerability reports and
797 organizational communications channels that are likely to receive vulnerability reports, such as
798 customer service and support.
```

The CVE database doesn't support this well, witness the 20,000+ missing SUSE URLs: https://github.com/distributedweaknessfiling/securitylist/commit/b690b4b1de7afba26c849e12b4aaadafc95e7e81 and 20,000+ missing Red Hat URLs: https://github.com/distributedweaknessfiling/securitylist/commit/e0a8925c90b1b4e6203fecbc6f61dcefe1b4accc and the hundreds (thousands?) of publicly used CVEs that are not in the database https://github.com/distributedweaknessfiling/securitylist/blob/main/missing-data/cvelist-missing-items-RESERVED-found-in-allitems.csv  or the CVEs in wide use for days or weeks (by the press even) prior to being entered into the CVE database.

Section: 799 3.2.3. Development of the Capability to Receive Vulnerability Disclosure Reports

```
800 Each VDPO should develop the capability to receive vulnerability reports from their associated
801 FCB participant. This includes the ability to communicate and enable coordination in
802 vulnerability reporting resolution, which requires the development of both technical and
803 personnel/procedural capabilities. If the FCB participant provides technical mechanisms to
804 streamline this process, the VDPO should use the provided mechanisms.
```

Where will these policies be published, and how will people find them? There are no generally accepted standards here, e.g. do they use domain.tld/security/ or domain.tld/.well-known/security.txt (https://securitytxt.org/) or simply rely on al ink in the front page or the "contact us" page? Discovery of how to report an issue is problematic and can result in people giving up and not reporting issues, or extra time being required during an emergency to find out whom to contact and how to contact them.

Section: 819 3.2.4. Development of Vulnerability Disclosure Handling Policies

```
820 Each VDPO should develop and maintain an internal vulnerability handling policy to define and
821 clarify its intentions for investigating and remediating vulnerabilities as part of a vulnerability
822 handling process. 
```

Is there any prescriptive help here, e.g. beyond ISO standards, any best practices for governments/agencies? It seems like a lot of reinventing the wheel will take place here, not all of it compatible or good. 

Section: 838 3.2.5.1. Receipt of Vulnerability Disclosure Reports

```
841 to identify the potentially vulnerable systems and software. Every vulnerability report should
842 have a priority rating, assigned by the FCB participant, that is used to optimize resource
843 allocations and determine the urgency of handling each report. If a VDPO permits the direct
```

No mention is made of any system to prioritize reports, e.g. is it severity times number of deployed systems times impact? There is no generally accepted guidance here, nor even a good list of the metrics or dimensions, e.g. vulnerability impact, PII exposure, operational requirements, etc. While prioritization is critical to direct resourcing appropriately the complete lack of any framework or guidelines is problematic. 

Section: 773 3.2.1. Development of Vulnerability Disclosure Report Acceptance Policies

```
786 The internal policy details the rules and procedures for handling, coordinating, and resolving
787 received vulnerability reports (further described in Section 3.1); the mechanisms used to track
788 reports; and expectations for communication with reporters and other stakeholders. It should
789 specify expected response and remediation timelines when handling vulnerability reports as well 
```

No mention is made of dealing with externally imposed deadlines, e.g. Google project 0 https://googleprojectzero.blogspot.com/2021/04/policy-and-disclosure-2021-edition.html and the lack of any guidance in the public policy may be problematic. This also dovetails with the publishing of metrics which are useful when reporting, e.g. is the entity responsive or slow?

Section: 846 3.2.5.2. Identification of Potentially Vulnerable Systems and Software

```
847 The first step to addressing a received vulnerability report is to identify the potentially vulnerable
848 software as well as the agency IT systems to which the report belongs. To enable this, each
849 VDPO should maintain a current list or database of contacts for each system within its purview.
850 In some cases, A VDPO that has received a vulnerability report may need to coordinate with
851 multiple system owners (or their security officer) to determine which system or software is
852 potentially vulnerable. This step does not involve verifying the existence of the vulnerability but
853 merely identifying to which system the report belongs.
854 Many products are complex systems that include or are dependent on other products or
855 components. Therefore, the initial analysis may not result in a clear understanding of which
856 products are affected by the vulnerability. It may take multiple iterations of discovery and
857 research before a determination can be made that the vulnerability exists within government858 produced software or commercial/open-source software used by the Government.
```

The lack of any prescriptive guidance or standards here is problematic and should be addressed (as evidenced by the direct mention of this very problem in the 2021-05-12 "Executive Order on Improving the Nation’s Cybersecurity" https://www.whitehouse.gov/briefing-room/presidential-actions/2021/05/12/executive-order-on-improving-the-nations-cybersecurity/ which mentions SBOM/etc.

Section: 955 3.3.4. Integration of Contractor Support into the VDPO

```
956 Policy considerations pertaining to the handling, resolution, and correction of vulnerability
957 disclosure information should be developed to include in any contracts that support an
958 information system in order to mitigate or resolve the vulnerability.
```

Guidance around the use of bug bounties especially will be needed here. 
