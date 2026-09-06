#!/usr/bin/env python3
"""Add D2 questions: State/local government, Bureaucracy, deeper Article structure, separation of powers."""
import sqlite3, json

DB = "fcle.db"

questions = [
    # State and local government (5)
    (2, "State and local government", "easy",
     "What is the primary source of power for state governments under the U.S. federal system?",
     "State governments derive their power from their state constitutions, which predate the U.S. Constitution.",
     json.dumps(["State governments receive all their authority directly from the U.S. Constitution.",
                  "State governments have only the powers that Congress explicitly grants them.",
                  "State governments operate under the authority of the President's executive orders."]),
     "State governments in the U.S. federal system derive their authority primarily from their own state constitutions. The original thirteen states existed before the federal government, and the Tenth Amendment reserves to the states all powers not delegated to the federal government. This means state governments have inherent police powers — the authority to regulate health, safety, welfare, and morals — that the federal government does not possess."),

    (2, "State and local government", "medium",
     "Which type of local government is the most common in the United States, and what is its primary function?",
     "Municipalities (cities and towns) are the most common; their primary function is providing local services like police, fire, water, and zoning.",
     json.dumps(["County governments are the most common; their primary function is managing federal programs in each state.",
                  "Special districts are the most common; their primary function is administering school systems.",
                  "Townships are the most common; their primary function is collecting federal taxes."]),
     "Municipalities — cities, towns, and villages — are the most numerous type of local government in the United States, with over 19,000 municipal governments. They are created under state law (Dillon's Rule states that local governments have only those powers explicitly granted by the state). Their primary functions include providing essential services such as police and fire protection, water and sewer systems, local road maintenance, zoning and land use regulation, and parks and recreation."),

    (2, "State and local government", "medium",
     "What is Dillon's Rule and how does it affect the relationship between state and local governments?",
     "Dillon's Rule holds that local governments have only those powers explicitly granted by the state government, making them subordinate to state authority.",
     json.dumps(["Dillon's Rule gives local governments the power to override state laws they disagree with.",
                  "Dillon's Rule establishes that local governments are co-equal with state governments under the Tenth Amendment.",
                  "Dillon's Rule requires the federal government to mediate disputes between states and their local governments."]),
     "Dillon's Rule, established by Judge John Forrest Dillon in the 1868 case Clinton v Cedar Rapids, holds that municipal governments are creatures of the state with only those powers expressly granted by state law, those necessarily implied by those granted powers, and those essential to the declared purposes of the corporation. Most states follow Dillon's Rule, meaning local governments cannot act unless the state has specifically authorized them to do so. Home rule cities have more autonomy."),

    (2, "State and local government", "hard",
     "What is the difference between Dillon's Rule and home rule, and why does this distinction matter for local governance?",
     "Dillon's Rule restricts local governments to only state-granted powers; home rule grants local governments broad authority to self-govern unless specifically prohibited by state law.",
     json.dumps(["Dillon's Rule applies to cities; home rule applies only to counties. The distinction determines which level handles federal programs.",
                  "Dillon's Rule requires state approval for all local ordinances; home rule eliminates the need for any state oversight whatsoever.",
                  "Both are the same concept; Dillon's Rule is simply the legal term for home rule charters."]),
     "The Dillon's Rule vs. home rule distinction fundamentally shapes local government authority. Under Dillon's Rule, local governments can only exercise powers that the state has explicitly granted. Under home rule (granted by state constitutions or statutes), local governments can act on any matter of local concern unless the state has specifically prohibited it. About 39 states allow some form of home rule. This distinction affects everything from minimum wage laws to environmental regulations to zoning."),

    (2, "State and local government", "easy",
     "What is a county government's primary role in the American federal system?",
     "Counties serve as administrative arms of the state, providing services like courts, law enforcement, public health, and record-keeping at the regional level.",
     json.dumps(["Counties are independent sovereign entities that can override both state and federal law.",
                  "Counties are federal administrative districts created by Congress to manage national elections.",
                  "Counties primarily exist to collect federal taxes and distribute them to municipalities."]),
     "County governments are the primary administrative divisions of most states, with over 3,000 counties in the United States. They typically serve as arms of the state government, administering state programs at the local level. Common county functions include maintaining courts and jails, operating sheriff's departments, conducting elections, recording property deeds, managing public health departments, and maintaining county roads and bridges."),

    # Bureaucracy (5)
    (2, "Bureaucracy", "easy",
     "What is the federal bureaucracy?",
     "The network of executive branch agencies, departments, and employees that implement and enforce federal laws and policies.",
     json.dumps(["The legislative branch committee system that drafts and reviews bills before they reach the full chamber.",
                  "The system of federal judges and their staffs who interpret the Constitution.",
                  "The network of state governors who coordinate federal policy implementation."]),
     "The federal bureaucracy refers to the organizations, agencies, and personnel of the executive branch that carry out the work of the federal government. This includes cabinet departments (like the Department of Education), independent agencies (like the EPA), regulatory commissions (like the FCC), and government corporations (like the Postal Service). Bureaucrats implement laws passed by Congress, enforce regulations, and provide public services."),

    (2, "Bureaucracy", "medium",
     "What is the difference between a cabinet department, an independent agency, and a regulatory commission?",
     "Cabinet departments are led by secretaries appointed by the President; independent agencies are outside the cabinet structure; regulatory commissions have quasi-legislative and quasi-judicial powers.",
     json.dumps(["There is no practical difference; all three are identical in structure and authority.",
                  "Cabinet departments are legislative; independent agencies are judicial; regulatory commissions are executive.",
                  "Cabinet departments handle foreign policy; independent agencies handle domestic policy; regulatory commissions handle military policy."]),
     "Cabinet departments (15 total) are the largest executive units, led by secretaries confirmed by the Senate, and organized into subunits. Independent agencies (like NASA, CIA) are outside the cabinet structure and typically have a single leader or board. Regulatory commissions (like the FCC, SEC) are independent of the President's direct control and have quasi-legislative power (making rules) and quasi-judicial power (adjudicating disputes), making them insulated from both presidential and congressional control."),

    (2, "Bureaucracy", "medium",
     "How do federal bureaucrats create regulations, and what is this process called?",
     "Federal agencies create regulations through a process called rulemaking, which involves public notice, comment periods, and final publication in the Federal Register.",
     json.dumps(["Bureaucrats create regulations by voting in secret sessions with no public input required.",
                  "Federal judges create regulations and instruct bureaucrats to enforce them.",
                  "Regulations are created exclusively by the President through executive orders."]),
     "Federal agencies create regulations through a process called 'informal rulemaking' or 'notice-and-comment rulemaking' under the Administrative Procedure Act (APA) of 1946. The process involves: (1) publishing a proposed rule in the Federal Register, (2) allowing a public comment period (typically 30-60 days), (3) reviewing comments and publishing a final rule, and (4) publishing the final rule in the Code of Federal Regulations. This gives the public a voice in how laws are implemented."),

    (2, "Bureaucracy", "hard",
     "What is 'iron triangle' in the context of federal bureaucracy, and why is it significant?",
     "An iron triangle is the close, mutually beneficial relationship between a bureaucratic agency, a congressional committee, and an interest group that influences policy in a specific area.",
     json.dumps(["An iron triangle refers to the three branches of government working together to pass legislation.",
                  "An iron triangle is a type of bureaucratic structure where three agencies share power over a single policy area.",
                  "An iron triangle is a legal doctrine that requires three levels of judicial review for agency actions."]),
     "The iron triangle model describes the stable, cooperative relationship among three actors in a policy area: a bureaucratic agency, the congressional committee that oversees and funds it, and the interest groups affected by its policies. These three groups develop a symbiotic relationship: the agency gets budget and political support from Congress and interest groups; Congress gets expertise and political support from the agency and interest groups; and interest groups get favorable policies from the agency and access through Congress."),

    (2, "Bureaucracy", "easy",
     "Who appoints the heads of federal cabinet departments?",
     "The President appoints them, and the Senate must confirm them.",
     json.dumps(["The Speaker of the House appoints them with House approval.",
                  "They are elected directly by the American people in midterm elections.",
                  "The Chief Justice of the Supreme Court nominates them."]),
     "The President nominates the heads of all 15 cabinet departments (known as secretaries, except for the Attorney General who heads the Department of Justice). The Senate must confirm these nominees by a majority vote. This confirmation process gives the legislative branch a check on the executive's ability to shape the bureaucracy. Cabinet secretaries serve at the pleasure of the President and can be removed at any time."),

    # Separation of powers (5)
    (2, "Separation of powers", "easy",
     "What is the principle of separation of powers?",
     "The division of government authority among three distinct branches — legislative, executive, and judicial — to prevent any single branch from becoming too powerful.",
     json.dumps(["The principle that all government power should be concentrated in the legislature.",
                  "The principle that the President has absolute authority over the other two branches.",
                  "The principle that state and federal governments must share all powers equally."]),
     "The separation of powers divides governmental authority into three distinct branches: the legislative branch (Congress, which makes laws), the executive branch (the President, who enforces laws), and the judicial branch (the courts, which interpret laws). This principle, derived from Montesquieu's Spirit of the Laws, is designed to prevent tyranny by ensuring that no single branch or person controls all governmental functions. The U.S. Constitution establishes this structure in Articles I, II, and III."),

    (2, "Separation of powers", "medium",
     "How does the system of checks and balances differ from the separation of powers?",
     "Separation of powers divides government into three branches with distinct functions; checks and balances gives each branch tools to limit the other branches' power.",
     json.dumps(["They are the same concept; there is no meaningful difference between them.",
                  "Separation of powers applies only to the federal government; checks and balances apply only to state governments.",
                  "Checks and balances is a British concept; separation of powers is an American concept."]),
     "While often used together, these are distinct concepts. Separation of powers divides government into three branches with distinct responsibilities (Congress legislates, the President executes, courts adjudicate). Checks and balances goes further by giving each branch constitutional tools to influence the other branches — for example, the President's veto over legislation, the Senate's confirmation power over judicial nominees, and the Supreme Court's power of judicial review. As Federalist No. 51 explains, 'ambition must be made to counteract ambition.'"),

    (2, "Separation of powers", "medium",
     "Which of the following is an example of the legislative branch checking the executive branch?",
     "The Senate's power to confirm or reject presidential appointments, including cabinet secretaries and federal judges.",
     json.dumps(["The President's power to veto bills passed by Congress.",
                  "The Supreme Court's power to declare executive actions unconstitutional.",
                  "The President's power to issue executive orders."]),
     "The Senate's advice and consent role is a key legislative check on executive power. The Constitution requires Senate confirmation for presidential appointments including cabinet secretaries, federal judges, ambassadors, and military officers. This gives the legislative branch significant influence over who serves in the executive branch and the judiciary. The House of Representatives also checks the executive through its power of impeachment, and both chambers check the executive through the power of the purse — controlling government spending."),

    (2, "Separation of powers", "hard",
     "What is the 'nondelegation doctrine' and how does it relate to the separation of powers?",
     "The nondelegation doctrine holds that Congress cannot delegate its legislative powers to other branches, limiting how much rulemaking authority agencies can exercise.",
     json.dumps(["The nondelegation doctrine requires the President to personally approve every regulation issued by federal agencies.",
                  "The nondelegation doctrine requires courts to make all administrative decisions without agency input.",
                  "The nondelegation doctrine prohibits any communication between the three branches of government."]),
     "The nondelegation doctrine is a principle of constitutional law holding that Congress, as the legislative branch, cannot delegate its lawmaking power to other branches or agencies. However, the Supreme Court has interpreted this doctrine very narrowly since the New Deal era, allowing Congress to delegate broad rulemaking authority to agencies as long as it provides an 'intelligible principle' to guide agency discretion. The Court has not struck down a federal law as an unconstitutional delegation since 1935."),

    (2, "Separation of powers", "easy",
     "Which article of the U.S. Constitution establishes the legislative branch?",
     "Article I.",
     json.dumps(["Article II",
                  "Article III",
                  "Article IV"]),
     "Article I of the U.S. Constitution establishes the legislative branch (Congress), consisting of a Senate and House of Representatives. It is the longest article of the Constitution and details Congress's powers, including taxation, borrowing, regulating commerce, declaring war, and the Necessary and Proper Clause. Placing the legislative branch first in the Constitution reflects the Framers' view that the legislature should be the primary and most powerful branch of government."),

    # Constitution Article structure (5)
    (2, "Article structure and content", "medium",
     "What does Article II of the U.S. Constitution establish?",
     "Article II establishes the executive branch, defining the powers and duties of the President.",
     json.dumps(["Article II establishes the judicial branch and the Supreme Court.",
                  "Article II establishes the process for amending the Constitution.",
                  "Article II establishes the relationship between state and federal governments."]),
     "Article II of the Constitution establishes the executive branch, vests executive power in the President, and defines the President's powers and duties. These include serving as Commander in Chief of the armed forces, making treaties (with Senate approval), appointing federal judges and executive officers (with Senate confirmation), granting pardons, and ensuring that laws are faithfully executed. Article II also establishes the Electoral College system for presidential elections and the Vice President's role."),

    (2, "Article structure and content", "medium",
     "What does Article III of the U.S. Constitution establish?",
     "Article III establishes the judicial branch, including the Supreme Court and such inferior courts as Congress may create.",
     json.dumps(["Article III establishes the legislative branch's committee system.",
                  "Article III establishes the process for ratifying amendments.",
                  "Article III establishes the President's cabinet and executive departments."]),
     "Article III establishes the judicial branch of the federal government. It creates the Supreme Court as the highest court and authorizes Congress to create lower federal courts. Article III defines the scope of judicial power, extends it to all 'cases and controversies,' and establishes that federal judges serve during good behavior (effectively for life). It also defines treason — the only crime specifically defined in the Constitution — and sets a high bar for conviction (testimony of two witnesses or confession in open court)."),

    (2, "Article structure and content", "easy",
     "What does Article IV of the U.S. Constitution address?",
     "Article IV addresses relations between states, including the Full Faith and Credit Clause and the Privileges and Immunities Clause.",
     json.dumps(["Article IV addresses the process for amending the Constitution.",
                  "Article IV establishes the Vice President's role in government.",
                  "Article IV creates the federal tax system."]),
     "Article IV contains provisions governing relations between states. The Full Faith and Credit Clause requires each state to recognize the laws, records, and court decisions of other states. The Privileges and Immunities Clause prevents states from discriminating against citizens of other states. Article IV also includes provisions for admitting new states, guarantees every state a republican form of government, and includes the Supremacy Clause's predecessor provisions about interstate relations."),

    (2, "Article structure and content", "medium",
     "What does Article V of the U.S. Constitution establish?",
     "Article V establishes the amendment process, allowing the Constitution to be changed through either congressional proposal or a constitutional convention.",
     json.dumps(["Article V establishes the process for electing members of Congress.",
                  "Article V creates the federal court system and judicial districts.",
                  "Article V defines the powers of the President during wartime."]),
     "Article V outlines two methods for proposing amendments and two methods for ratification. Amendments may be proposed by a two-thirds vote of both houses of Congress or by a national convention called by two-thirds of state legislatures (this second method has never been used). Amendments may be ratified by three-fourths of state legislatures or by conventions in three-fourths of the states. This deliberately difficult process ensures that the Constitution is changed only with broad national consensus."),

    (2, "Article structure and content", "easy",
     "How many articles are in the original U.S. Constitution?",
     "Seven articles.",
     json.dumps(["Ten articles",
                  "Five articles",
                  "Twelve articles"]),
     "The original U.S. Constitution contains seven articles: Article I (Legislative Branch), Article II (Executive Branch), Article III (Judicial Branch), Article IV (States' Relations), Article V (Amendment Process), Article VI (Supremacy Clause and Debts), and Article VII (Ratification). The first ten amendments, known as the Bill of Rights, were added in 1791 but are not part of the original seven articles. The Constitution is the oldest written and codified national constitution still in force today."),
]

conn = sqlite3.connect(DB)
cur = conn.cursor()
for q in questions:
    cur.execute(
        "INSERT INTO questions (fcle_domain, topic, difficulty, question, correct_answer, wrong_answers, explanation) VALUES (?,?,?,?,?,?,?)",
        q
    )
conn.commit()
print(f"Inserted {len(questions)} D2 questions")
conn.close()
