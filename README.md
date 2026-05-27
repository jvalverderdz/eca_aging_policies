This note outlines the process for consolidating, processing and summarizing the Madrid International Plans of Action on Ageing for ECA countries. The goal of the algorithm is to generate concise and reliable answers to a series of questions regarding the planning, implementation and status of policies on ageing in ECA countries. This is consolidated in the following questions:
1.	Is there an aging strategy in place?
2.	Is there a designated agency/ministry in charge of coordinating aging-related policies?
3.	Are strategies on aging accompanied by an action plan?
4.	How do the strategy and policies help recognize the potential of older persons?
5.	What strategies legislative frameworks policy guidelines and planning instruments exist to ensure full integration and participation of older persons in society?
6.	What specific policy actions government programs implemented and measurable outcomes have been achieved to ensure full integration and participation of older persons in society?
7.	What strategies legislative frameworks policy guidelines and planning instruments exist to promote equitable and sustainable economic growth in response to population ageing?
8.	What specific policy actions government programs implemented and measurable outcomes have been achieved to promote equitable and sustainable economic growth in response to population ageing?
9.	What strategies legislative frameworks policy guidelines and planning instruments exist to adjust social protection systems in response to demographic changes and their social and economic consequences?
10.	What specific policy actions government programs implemented and measurable outcomes have been achieved to adjust social protection systems in response to demographic changes and their social and economic consequences?
11.	What strategies legislative frameworks policy guidelines and planning instruments exist to enable labour markets to respond to the economic and social consequences of population ageing?
12.	What specific policy actions government programs implemented and measurable outcomes have been achieved to enable labour markets to respond to the economic and social consequences of population ageing?
13.	What strategies legislative frameworks policy guidelines and planning instruments exist to promote lifelong learning and adapt the educational system to changing economic social and demographic conditions?
14.	What specific policy actions government programs implemented and measurable outcomes have been achieved to promote lifelong learning and adapt the educational system to changing economic social and demographic conditions?
15.	What strategies legislative frameworks policy guidelines and planning instruments exist to ensure quality of life at all ages and maintain independent living including health and well-being?
16.	What specific policy actions government programs implemented and measurable outcomes have been achieved to ensure quality of life at all ages and maintain independent living including health and well-being?
17.	What strategies legislative frameworks policy guidelines and planning instruments exist to mainstream a gender approach in an ageing society?
18.	What specific policy actions government programs implemented and measurable outcomes have been achieved to mainstream a gender approach in an ageing society?
19.	What strategies legislative frameworks policy guidelines and planning instruments exist to support families that provide care for older persons and promote intergenerational and intragenerational solidarity?
20.	What specific policy actions government programs implemented and measurable outcomes have been achieved to support families that provide care for older persons and promote intergenerational and intragenerational solidarity?
21.	What strategies legislative frameworks policy guidelines and planning instruments exist to promote the implementation and follow-up of the Regional Implementation Strategy through regional cooperation?
22.	What specific policy actions government programs implemented and measurable outcomes have been achieved to promote the implementation and follow-up of the Regional Implementation Strategy through regional cooperation?
23.	What strategies legislative frameworks policy guidelines and planning instruments empower individuals to realise their potential for physical mental and social well-being?
24.	What specific policy actions government programs implemented and measurable outcomes empower individuals to realise their potential for physical mental and social well-being?
25.	What strategies legislative frameworks policy guidelines and planning instruments promote the social participation of older persons?
26.	What specific policy actions government programs implemented and measurable outcomes promote the social participation of older persons?
27.	What strategies legislative frameworks policy guidelines and planning instruments promote the participation of older persons in decision-making?
28.	What specific policy actions government programs implemented and measurable outcomes promote the participation of older persons in decision-making?
29.	What strategies legislative frameworks policy guidelines and planning instruments promote a positive image of older persons aknowledging their contributions to society and strengthening multigenerational discourse?
30.	What specific policy actions government programs implemented and measurable outcomes promote a positive image of older persons aknowledging their contributions to society and strengthening multigenerational discourse?
31.	What strategies legislative frameworks policy guidelines and planning instruments promote age-friendly environments cities and communities and accessibility for older people?
32.	What specific policy actions government programs implemented and measurable outcomes promote age-friendly environments cities and communities and accessibility for older people?
33.	What strategies legislative frameworks policy guidelines and planning instruments promote engagement of older persons as consumers?
34.	What specific policy actions government programs implemented and measurable outcomes promote engagement of older persons as consumers?
35.	What strategies legislative frameworks policy guidelines and planning instruments foster access to and promotion of lifelong learning opportunities and development of skills for all ages?
36.	What specific policy actions government programs implemented and measurable outcomes foster access to and promotion of lifelong learning opportunities and development of skills for all ages?
37.	What strategies legislative frameworks policy guidelines and planning instruments exist to fight unemployment at all ages?
38.	What specific policy actions government programs implemented and measurable outcomes have been achieved to fight unemployment at all ages?
39.	What strategies legislative frameworks policy guidelines and planning instruments exist to reduce old-age poverty?
40.	What specific policy actions government programs implemented and measurable outcomes have been achieved to reduce old-age poverty?
41.	What strategies legislative frameworks policy guidelines and planning instruments exist to prevent age-related discrimination in employment?
42.	What specific policy actions government programs implemented and measurable outcomes have been achieved to prevent age-related discrimination in employment?
43.	What strategies legislative frameworks policy guidelines and planning instruments exist for pension reform?
44.	What specific policy actions government programs implemented and measurable outcomes have been achieved in pension reform?
45.	What is the adequacy and sustainability of the pensions system?
46.	What is the support for research on individual and population ageing processes to address emerging needs in ageing societies especially with respect to dementia or mental and behavioural disorders?
47.	How does this country promote self-determination in palliative care and at the end of life?


  
The process of generating an automated response to these questions is as follows:
1)	Download country MIPAA reports PDF files. This is conducted manually, as the UNECE website is blocked against automatized scraping. 44 files are downloaded.
2)	OCR Processing (when necessary). Scanned PDFs are processed through an OCR tool that transforms images into parsable text.
3)	Translation (when necessary). Files not in English are translated to English using the Document Translation tool by Google Translate.
4)	PDF Files are transformed to TXT Files to facilitate reading and loading by Python.
From here on, two approaches are used: One, entirely reliant on Agentic IAs to produce a Search of the whole texts to answer the questions. The other, pre-processes the files and conducts a preliminary Semantic Search to provide the Agent with only the relevant chunks of the reports, ensuring a faster, cheaper, and more reliable answer. The second approach is described:
5)	TXT Files are divided in Chunks. Each Chunk comprises approximately one paragraph of text.
6)	A Natural Language Processing (NLP) algorithm is applied to each Chunk to embed it into a multi-dimensional vector space, such that more phrases more similar in context and meaning appear “closer” to each other.
a.	Parallelly, the text of the questions is similarly embedded into the same vector space, such that the answers to such questions will appear “closer” to them.
7)	A Semantic Search is Conducted for each question. This is carried out by comparing the cosine similarities of the question and all Chunks; selecting the values that are larger, indicating similar contexts and meanings. The Chunks with the top 10 values are selected.
8)	Finally, the 10 Chunks that are estimated to have the answers for each question are provided to an Agentic IA (Claude Sonnet 4.6) to generate a one-paragraph summary of their contents.


