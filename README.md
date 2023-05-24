Using the Open Editors data to explore journal editorship in UK Universities

# REF2021 data 

The REF provides data on evaluation of University research outputs and environments. You can *crudely* position institutions by the average (median) score their received in the REF across all the units of assessment (roughly, 'disciplines') they submitted.

Institutions also differered in how many research staff they have / they submitted. The largest was University of Oxford, which submitted ~3400 FTE staff. See <https://github.com/tomstafford/ref2021>

# Open Editor Data

Open Editors project <https://openeditors.ooir.org/> scrapes data on journal editors and their affiliations.

The data is messy, often out of data and incomplete. Some publishers (e.g. Taylor and Francis) are not checked. Some editors list their affiliations inconsistency. For my data. this means that institutions with more variations on their name will be undercounted (e.g. LSE could be "LSE", "London School of Economics","The London School of Economics and Political Science", etc)

Reference: Nishikawa-Pacher, Andreas, Tamara Heck and Kerstin Schoch (2022), "Open Editors: A Dataset of Scholarly Journals’ Editorial Board Positions", Research Evaluation, DOI: 10.1093/reseval/rvac037. 

# Nonetheless

It is interesting to try to understand the institutional context of journal editing. Like reviewing, journal editing is often underrecognised and only indirectly rewarded by institutions. It comes with some prestige and influence, but also adds work to academics who have many competing obligations.

For an initial investigation, I plotted REF score against proportion of journal editors (almost always a value below 1, indicating that institutions invariably have more staff than they have staff who are also editors). 

![](figs/gpa_vs_eds.png)

I made a [crude version with rollover functionality](https://tomstafford.github.io/editors/figs/plotly.html), so you can pick out your favourite UK institutions. Imperial is in the top right, UCL is the large blop nearly as high up the y axis. Oxford is the largest blob, on the x=3.5 line. 


# Caveats

My analysis "double-counts" individuals who are editors on more than one journal

There's more to life than REF scores (but you might not know it from the way some institutional processes work)


# Next?

I'm thinking about what else to do with these data, so feedback is welcome, by email or to [@tomstafford](https://mastodon.online/@tomstafford)

Repo: <https://github.com/tomstafford/editors>

# Updates

## 2023-05-24

Lizzie Gadd asks what the plot would look like if it was only the 'environment' component of the REF on the x-axis. Here we are

![](figs/ENVgpa_vs_eds.png)

Rollover version [here](figs/plotlyENV.html)
