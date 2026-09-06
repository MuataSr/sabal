#!/usr/bin/env python3
"""Add D4 questions batch 4: 21 more (heavy on hard) to reach 150."""
import sqlite3, json

DB = "fcle.db"

questions = [
    # Hard: landmark cases deeper (8)
    (4, "Landmark cases", "hard",
     "What was the legal principle established in McCulloch v Maryland (1819), and how does it affect federal power today?",
     "Congress has implied powers under the Necessary and Proper Clause, and states cannot tax federal institutions — significantly expanding federal authority.",
     json.dumps(["States can tax federal institutions without limitation, strengthening state power.",
                  "Congress has no implied powers and can only exercise those explicitly listed in the Constitution.",
                  "The federal government can tax state institutions but states cannot tax the federal government."]),
     "In McCulloch v Maryland (1819), the Supreme Court established two principles that remain foundational. First, Congress has implied powers — powers not explicitly listed but 'necessary and proper' for carrying out its enumerated powers. The Court held that 'necessary' means 'convenient or useful,' not absolutely indispensable, allowing Congress to create a national bank. Second, states cannot tax federal institutions because 'the power to tax is the power to destroy.' Together, these principles significantly expanded federal authority and remain central to debates about the scope of congressional power and federal immunity from state regulation."),

    (4, "Landmark cases", "hard",
     "How did Baker v Carr (1962) revolutionize American democracy through the 'one person, one vote' principle?",
     "The Court ruled that federal courts have jurisdiction over legislative apportionment, leading to rulings that required electoral districts to be roughly equal in population.",
     json.dumps(["Baker v Carr established that corporations have the same voting rights as individual citizens.",
                  "Baker v Carr had no significant impact on American electoral systems.",
                  "Baker v Carr eliminated the Electoral College and established direct popular voting for all elections."]),
     "Baker v Carr (1962) opened the door for federal courts to address legislative apportionment. Before Baker, the Court considered apportionment a 'political question' beyond judicial review. The case led to a series of decisions establishing the 'one person, one vote' principle: Reynolds v Sims (1964) required state legislative districts to be equal in population, and Wesberry v Sanders (1964) applied the same principle to congressional districts. These decisions transformed American democracy by ending the practice of rural overrepresentation, where rural areas with small populations had the same representation as urban areas with much larger populations."),

    (4, "Landmark cases", "hard",
     "What was the significance of Gideon v Wainwright (1963) for criminal justice in America?",
     "The Court held that the Sixth Amendment's right to counsel applies to all criminal defendants in felony cases, even those who cannot afford an attorney, requiring states to provide court-appointed lawyers.",
     json.dumps(["Gideon held that defendants must represent themselves without any legal assistance.",
                  "Gideon limited the right to counsel to only federal cases, not state prosecutions.",
                  "Gideon held that only wealthy defendants have the right to hire attorneys."]),
     "Gideon v Wainwright (1963) incorporated the Sixth Amendment's right to counsel against the states, requiring that indigent defendants in felony cases be provided with court-appointed attorneys. Clarence Earl Gideon, a poor man accused of breaking into a pool hall, was forced to defend himself at trial and was convicted. He handwrote a petition to the Supreme Court, which unanimously ruled that the right to counsel is fundamental to a fair trial. The decision led to the creation of the public defender system and dramatically changed criminal justice in America, ensuring that wealth does not determine access to legal representation."),

    (4, "Landmark cases", "hard",
     "How did the Lemon test (Lemon v Kurtzman, 1971) evaluate whether government actions violate the Establishment Clause?",
     "A law must have a secular purpose, not primarily advance or inhibit religion, and not create excessive government entanglement with religion.",
     json.dumps(["The Lemon test requires that all government actions must promote religion to be constitutional.",
                  "The Lemon test applies only to the Free Exercise Clause, not the Establishment Clause.",
                  "The Lemon test was immediately rejected by the Supreme Court and never applied."]),
     "The Lemon test, established in Lemon v Kurtzman (1971), provided a three-part test for whether government action violates the Establishment Clause: (1) the statute must have a secular legislative purpose, (2) its principal or primary effect must be one that neither advances nor inhibits religion, and (3) it must not foster excessive government entanglement with religion. The Lemon test guided Establishment Clause analysis for decades, though the Supreme Court has modified its approach in recent years. Critics argued it was too rigid and inconsistent; supporters argued it provided necessary clarity for church-state separation."),

    (4, "Landmark cases", "hard",
     "What is 'strict scrutiny' and when does the Supreme Court apply it?",
     "Strict scrutiny is the highest level of judicial review, applied when a law infringes on a fundamental right or involves a suspect classification like race; the government must show the law is narrowly tailored to serve a compelling government interest.",
     json.dumps(["Strict scrutiny applies to all laws equally regardless of the right involved.",
                  "Strict scrutiny is the lowest level of review, requiring only that the law be reasonable.",
                  "Strict scrutiny was abolished by the Supreme Court in 2000 and is no longer used."]),
     "Strict scrutiny is the most rigorous standard of judicial review used by American courts. It applies in two situations: when a law infringes a fundamental constitutional right, or when a law involves a suspect classification (race, national origin, and sometimes religion). Under strict scrutiny, the government bears the burden of proving that the law is narrowly tailored to serve a compelling government interest — the most demanding standard in constitutional law. Laws that survive strict scrutiny are rare. By contrast, intermediate scrutiny applies to gender classifications, and rational basis review applies to most other laws."),

    (4, "Landmark cases", "hard",
     "What was the significance of Obergefell v Hodges (2015) for civil rights in America?",
     "The Court ruled that same-sex couples have a fundamental right to marry under the Fourteenth Amendment's Due Process and Equal Protection Clauses, legalizing same-sex marriage nationwide.",
     json.dumps(["Obergefell ruled that marriage is only between a man and a woman and overturned same-sex marriage.",
                  "Obergefell had no effect on marriage law because marriage is regulated exclusively by states.",
                  "Obergefell established civil unions but stopped short of legalizing same-sex marriage."]),
     "Obergefell v Hodges (2015) was a landmark civil rights decision in which the Supreme Court held 5-4 that the Fourteenth Amendment requires states to license marriages between same-sex couples and to recognize same-sex marriages performed in other states. Justice Kennedy's majority opinion found that the right to marry is a fundamental liberty protected by the Due Process Clause and that denying same-sex couples this right violates the Equal Protection Clause. The decision built on precedents including Lawrence v Texas (2003) and United States v Windsor (2013), which had progressively expanded LGBT rights."),

    (4, "Landmark cases", "hard",
     "How did Griswold v Connecticut (1965) establish a constitutional right to privacy?",
     "The Court found a right to privacy in the 'penumbras' of the Bill of Rights, striking down a Connecticut law banning contraceptives for married couples.",
     json.dumps(["Griswold held that there is no right to privacy in the Constitution and upheld the Connecticut law.",
                  "Griswold found a right to privacy only in the Fourth Amendment's search and seizure clause.",
                  "Griswold was about property rights, not personal privacy."]),
     "In Griswold v Connecticut (1965), the Supreme Court struck down a Connecticut law that banned the use of contraceptives by married couples. Justice Douglas's majority opinion found a right to marital privacy in the 'penumbras' — the shadows or zones — created by several amendments in the Bill of Rights. While no single amendment explicitly protects privacy, the Court found that the First, Third, Fourth, Fifth, and Ninth Amendments together create 'zones of privacy.' This right to privacy became the foundation for later decisions including Roe v Wade (abortion), Lawrence v Texas (sexual intimacy), and Obergefell v Hodges (same-sex marriage)."),

    (4, "Landmark cases", "hard",
     "What is the distinction between de jure segregation and de facto segregation, and which did Brown v Board address?",
     "De jure segregation is segregation required by law; de facto segregation results from social and economic factors. Brown v Board addressed de jure segregation.",
     json.dumps(["Brown v Board addressed de facto segregation but had no effect on de jure segregation.",
                  "There is no distinction between de jure and de facto segregation; they are identical.",
                  "Brown v Board addressed both de jure and de facto segregation simultaneously with equal force."]),
     "De jure segregation (segregation by law) was the system of legally mandated racial separation enforced primarily in the Southern states through laws requiring separate schools, facilities, and services. De facto segregation (segregation in fact) results from housing patterns, economic inequality, and social factors rather than legal requirements. Brown v Board of Education (1954) specifically addressed de jure segregation, ruling that laws requiring separate schools based on race violate the Equal Protection Clause. Distinguishing between de jure and de facto segregation became important in later cases because the Court's remedies for legally mandated segregation were more aggressive than those for segregation resulting from private choices."),

    # Hard: civil rights movement cases (6)
    (4, "Civil rights movement", "hard",
     "How did the Civil Rights Act of 1964 expand federal power to combat discrimination?",
     "It prohibited discrimination in employment, public accommodations, and federally funded programs, using the Commerce Clause and Congress's spending power as constitutional authority.",
     json.dumps(["It had no constitutional basis and relied solely on executive orders with no legal authority.",
                  "It only addressed voting rights and had no provisions regarding employment or public accommodations.",
                  "It was struck down by the Supreme Court as unconstitutional within a year of passage."]),
     "The Civil Rights Act of 1964 was the most comprehensive civil rights legislation since Reconstruction. Title II prohibited discrimination in public accommodations (hotels, restaurants, theaters) using the Commerce Clause as constitutional authority. Title VII prohibited employment discrimination based on race, color, religion, sex, or national origin. Title VI prohibited discrimination in federally funded programs. The Supreme Court upheld the law in Heart of Atlanta Motel v United States (1964), ruling that Congress could use its Commerce Clause power to prohibit racial discrimination by businesses engaged in interstate commerce."),

    (4, "Civil rights movement", "hard",
     "How did the Voting Rights Act of 1965 address voting discrimination, and what made it effective?",
     "It banned literacy tests and authorized federal oversight of jurisdictions with histories of voting discrimination through a 'preclearance' requirement under Section 5.",
     json.dumps(["It simply encouraged states to allow Black Americans to vote without any enforcement mechanisms.",
                  "It eliminated all voting restrictions for all citizens regardless of circumstance.",
                  "It was a symbolic declaration with no practical effect on voting practices."]),
     "The Voting Rights Act of 1965 was the most effective piece of civil rights legislation in American history. It banned literacy tests and other discriminatory voting requirements. Its most powerful provision was Section 5, which required jurisdictions with histories of voting discrimination (primarily Southern states) to obtain 'preclearance' from the federal government before changing their voting laws. This prevented states from finding new ways to disenfranchise minority voters. Black voter registration in Mississippi increased from 6.7% to 59.8% within four years. In Shelby County v Holder (2013), the Supreme Court struck down the preclearance formula."),

    (4, "Civil rights movement", "medium",
     "What was the Montgomery Bus Boycott, and what role did it play in the civil rights movement?",
     "A 381-day boycott of Montgomery, Alabama's buses after Rosa Parks' arrest in 1955; it demonstrated the power of nonviolent protest and launched Dr. Martin Luther King Jr.'s national leadership.",
     json.dumps(["It was a one-day event that had no lasting impact on the civil rights movement.",
                  "It was a violent uprising that forced the federal government to send troops to Alabama.",
                  "It was a boycott of federal government buildings organized by the NAACP."]),
     "The Montgomery Bus Boycott (December 1955 — December 1956) began when Rosa Parks, a Black woman, refused to give up her seat to a white passenger on a Montgomery city bus. Her arrest sparked a boycott of the bus system organized by the Montgomery Improvement Association, led by a young minister named Dr. Martin Luther King Jr. For 381 days, Black residents carpooled, walked, or used Black-owned taxis rather than ride the segregated buses. The boycott ended when the Supreme Court ruled in Browder v Gayle (1956) that Montgomery's bus segregation was unconstitutional. The boycott demonstrated the power of nonviolent direct action."),

    (4, "Civil rights movement", "medium",
     "What was the significance of the March on Washington (1963)?",
     "It was a massive peaceful demonstration where Dr. Martin Luther King Jr. delivered his 'I Have a Dream' speech, building public support for the Civil Rights Act of 1964.",
     json.dumps(["It was a violent riot that led to the arrest of over 10,000 protesters.",
                  "It was a small meeting of civil rights leaders with no public audience.",
                  "It was a march demanding the repeal of the Civil Rights Act."]),
     "The March on Washington for Jobs and Freedom on August 28, 1963, was one of the largest political rallies in American history, with approximately 250,000 attendees. It was organized by civil rights leaders including A. Philip Randolph, Bayard Rustin, and Dr. Martin Luther King Jr. King's 'I Have a Dream' speech, delivered from the steps of the Lincoln Memorial, became one of the most famous speeches in American history and a defining moment of the civil rights movement. The march built public support for the civil rights legislation that President Kennedy had proposed, contributing to the passage of the Civil Rights Act of 1964 after Kennedy's assassination."),

    (4, "Civil rights movement", "medium",
     "What was the role of the NAACP in the civil rights movement?",
     "The NAACP used legal strategies, particularly litigation, to challenge segregation and discrimination, culminating in Brown v Board of Education and other landmark cases.",
     json.dumps(["The NAACP organized violent protests and armed resistance against segregation laws.",
                  "The NAACP was a government agency created by Congress to enforce civil rights.",
                  "The NAACP focused exclusively on economic issues and had no involvement in legal challenges to segregation."]),
     "The National Association for the Advancement of Colored People (NAACP), founded in 1909, was the most important civil rights organization of the 20th century. Its legal strategy, led by attorneys including Thurgood Marshall (who later became the first Black Supreme Court justice), used the courts to challenge segregation and discrimination. The NAACP's Legal Defense Fund brought the cases that gradually dismantled legal segregation: challenging graduate school segregation (Missouri ex rel. Gaines v Canada, 1938), winning equal pay for Black teachers, and ultimately winning Brown v Board of Education (1954). The NAACP's legal victories laid the groundwork for the broader civil rights movement."),

    (4, "Civil rights movement", "medium",
     "What were 'Jim Crow laws' and when were they enacted?",
     "State and local laws enforcing racial segregation in the Southern United States, enacted primarily in the late 19th and early 20th centuries after Reconstruction.",
     json.dumps(["Jim Crow laws were federal laws passed in the 1960s to promote racial equality.",
                  "Jim Crow laws were Northern state laws that prohibited all forms of racial discrimination.",
                  "Jim Crow laws were international treaties that governed trade between the US and European nations."]),
     "Jim Crow laws were state and local statutes enacted primarily in the Southern states between the 1870s and 1960s that mandated racial segregation in virtually all aspects of public life. Named after a racist minstrel show character, these laws required separate schools, hospitals, prisons, parks, restaurants, buses, trains, water fountains, restrooms, and even cemeteries for Black and white Americans. The Supreme Court's 'separate but equal' ruling in Plessy v Ferguson (1896) gave Jim Crow laws constitutional cover. They were dismantled through the civil rights movement and legislation including Brown v Board (1954), the Civil Rights Act (1964), and the Voting Rights Act (1965)."),

    # Medium: additional governance (7)
    (4, "Civil liberties", "medium",
     "What does the Eighth Amendment protect against?",
     "Cruel and unusual punishment and excessive bail and fines.",
     json.dumps(["Unreasonable searches and seizures.",
                  "Self-incrimination and double jeopardy.",
                  "Quartering of soldiers in private homes."]),
     "The Eighth Amendment states: 'Excessive bail shall not be required, nor excessive fines imposed, nor cruel and unusual punishments inflicted.' The 'cruel and unusual punishment' clause has been the most litigated, addressing issues including the death penalty (Furman v Georgia, 1972; Gregg v Georgia, 1976), conditions of confinement, mandatory life sentences for juveniles (Miller v Alabama, 2012), and execution methods. The Supreme Court has held that the Eighth Amendment's prohibition of cruel and unusual punishment must be interpreted according to 'evolving standards of decency' — meaning its meaning changes as society's values change."),

    (4, "Civil liberties", "medium",
     "What does the Establishment Clause prohibit, and what is the 'wall of separation between church and state'?",
     "The Establishment Clause prohibits the government from establishing an official religion or favoring one religion over others; the 'wall of separation' metaphor was coined by Thomas Jefferson.",
     json.dumps(["The Establishment Clause requires the government to actively promote religion in all public institutions.",
                  "The Establishment Clause prohibits all religious expression in any public space.",
                  "The Establishment Clause only applies to state governments, not the federal government."]),
     "The Establishment Clause of the First Amendment — 'Congress shall make no law respecting an establishment of religion' — prohibits the government from establishing an official religion, favoring one religion over others, or excessively entangling government with religion. Thomas Jefferson coined the metaphor 'wall of separation between Church and State' in an 1802 letter to the Danbury Baptists, explaining that the First Amendment built 'a wall of separation between Church and State.' The Supreme Court has referenced this metaphor in numerous decisions, though the exact boundary between church and state remains a subject of ongoing litigation and debate."),

    (4, "Civil liberties", "medium",
     "What is the difference between the Free Exercise Clause and the Establishment Clause of the First Amendment?",
     "The Free Exercise Clause protects individuals' right to practice their religion; the Establishment Clause prevents the government from promoting or establishing religion.",
     json.dumps(["Both clauses do the same thing — they both prohibit all forms of religious practice.",
                  "The Free Exercise Clause allows the government to control religious practices; the Establishment Clause has no practical effect.",
                  "There is only one religion clause in the First Amendment, not two."]),
     "The First Amendment contains two religion clauses that pull in opposite directions. The Free Exercise Clause protects individuals' right to practice their religion (or no religion) without government interference. The Establishment Clause prevents the government from promoting, endorsing, or establishing religion. Balancing these two clauses creates ongoing tension: protecting religious freedom (Free Exercise) without allowing the government to favor religion (Establishment). For example, a public school cannot lead students in prayer (Establishment Clause) but must accommodate students' religious practices to the extent possible (Free Exercise Clause)."),

    (4, "Governance", "medium",
     "What is the process for impeaching and removing a federal official?",
     "The House impeaches (brings charges) by majority vote; the Senate tries the case and convicts by two-thirds vote; the Chief Justice presides when the President is tried.",
     json.dumps(["Impeachment requires a unanimous vote of both houses of Congress and approval by the Supreme Court.",
                  "Only the President can be impeached; other federal officials are immune from impeachment.",
                  "Impeachment is handled entirely by the judicial branch with no congressional involvement."]),
     "The impeachment process has two stages. First, the House of Representatives impeaches an official by passing articles of impeachment (a simple majority vote). Impeachment is analogous to an indictment — it brings charges but does not remove the official. Second, the Senate holds a trial to determine whether to convict and remove the official from office. A two-thirds majority is required for conviction. When the President is tried, the Chief Justice of the Supreme Court presides. Impeachment is limited to removal from office and potential disqualification from future office; criminal prosecution can follow separately. Three Presidents have been impeached (Andrew Johnson, Bill Clinton, Donald Trump); none have been convicted."),

    (4, "Governance", "medium",
     "What is the Supremacy Clause, and what does it establish?",
     "Article VI, Clause 2 establishes that the Constitution, federal laws, and treaties are the supreme law of the land, overriding conflicting state laws.",
     json.dumps(["The Supremacy Clause gives state governments the power to override federal laws.",
                  "The Supremacy Clause establishes that the President has supreme authority over all branches of government.",
                  "The Supremacy Clause was repealed by the Tenth Amendment and no longer applies."]),
     "The Supremacy Clause (Article VI, Clause 2) states: 'This Constitution, and the Laws of the United States which shall be made in Pursuance thereof; and all Treaties made... shall be the supreme Law of the Land; and the Judges in every State shall be bound thereby.' This clause resolves conflicts between federal and state law in favor of federal law, establishing the principle of national supremacy. However, the clause only applies to laws made 'in pursuance' of the Constitution — federal laws that themselves violate the Constitution are not supreme and can be struck down by courts."),

    (4, "Governance", "medium",
     "What is the difference between civil liberties and civil rights?",
     "Civil liberties protect individuals from government interference (free speech, religion, due process); civil rights protect individuals from discrimination by the government or private actors.",
     json.dumps(["Civil liberties and civil rights are the same concept with no meaningful difference.",
                  "Civil liberties apply only to citizens; civil rights apply only to non-citizens.",
                  "Civil liberties are granted by the President; civil rights are granted by Congress."]),
     "Civil liberties are protections from government action — they limit what the government can do to individuals. Examples include freedom of speech, freedom of religion, the right to due process, and protection against unreasonable searches. Civil rights are protections against discrimination — they ensure equal treatment under the law regardless of race, gender, religion, or other characteristics. Examples include the right to vote, the right to equal employment opportunities, and the right to access public accommodations. Civil liberties are primarily found in the Bill of Rights; civil rights are primarily found in the Civil Rights Act, Voting Rights Act, and Equal Protection Clause."),

    (4, "Governance", "medium",
     "What is the difference between a constitutional right and a statutory right?",
     "Constitutional rights are protected by the Constitution and cannot be easily changed; statutory rights are created by legislation and can be modified or repealed by the legislature.",
     json.dumps(["There is no difference; all rights are equally protected and equally permanent.",
                  "Statutory rights are superior to constitutional rights and can override them.",
                  "Constitutional rights are temporary; statutory rights are permanent."]),
     "Constitutional rights are protections guaranteed by the U.S. Constitution and can only be changed through the difficult amendment process (two-thirds of Congress plus three-fourths of states). This makes them relatively permanent and difficult to alter. Statutory rights are created by federal, state, or local legislation and can be modified, expanded, or repealed by the legislature that created them. For example, the right to free speech is a constitutional right that cannot be repealed by Congress, while the right to family leave under the Family and Medical Leave Act is a statutory right that Congress could modify or repeal through ordinary legislation."),
]

conn = sqlite3.connect(DB)
cur = conn.cursor()
for q in questions:
    cur.execute(
        "INSERT INTO questions (fcle_domain, topic, difficulty, question, correct_answer, wrong_answers, explanation) VALUES (?,?,?,?,?,?,?)",
        q
    )
conn.commit()
print(f"Inserted {len(questions)} D4 questions")
conn.close()
