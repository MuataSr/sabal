#!/usr/bin/env python3
"""Add D2 (4) and D3 (7) questions to reach 150 each."""
import sqlite3, json

DB = "fcle.db"

questions = [
    # D2 — 4 more
    (2, "Key amendments", "medium",
     "What did the Twenty-Fourth Amendment eliminate, and why was it significant?",
     "It eliminated poll taxes in federal elections, removing a barrier that prevented poor and minority voters from participating.",
     json.dumps(["It eliminated the Electoral College in favor of direct popular vote for President.",
                  "It eliminated the requirement that voters be property owners.",
                  "It eliminated term limits for members of Congress."]),
     "The Twenty-Fourth Amendment, ratified in 1964, states: 'The right of citizens of the United States to vote in any primary or other election for President or Vice President... shall not be denied or abridged... by reason of failure to pay any poll tax or other tax.' Several Southern states had used poll taxes to disenfranchise Black voters, who were disproportionately poor. The amendment removed this barrier to voting in federal elections. The Supreme Court later extended the prohibition to state elections in Harper v Virginia Board of Elections (1966), ruling that wealth cannot be a qualification for voting."),

    (2, "Key amendments", "hard",
     "What is the significance of the Reconstruction Amendments (Thirteenth, Fourteenth, and Fifteenth), and how did they transform the Constitution?",
     "They abolished slavery (13th), established birthright citizenship and equal protection (14th), and prohibited racial discrimination in voting (15th) — fundamentally redefining American citizenship and federal power.",
     json.dumps(["They primarily dealt with economic regulation and had little effect on civil rights.",
                  "They temporarily suspended the Constitution during wartime and were later repealed.",
                  "They strengthened state sovereignty by returning all powers to state governments."]),
     "The Reconstruction Amendments — the Thirteenth (1865), Fourteenth (1868), and Fifteenth (1870) — represent the second founding of American constitutional law. The Thirteenth Amendment abolished slavery, overturning Dred Scott. The Fourteenth Amendment introduced birthright citizenship, the Privileges or Immunities Clause, the Due Process Clause, and the Equal Protection Clause — becoming the most litigated amendment in constitutional law. The Fifteenth Amendment prohibited denying the right to vote based on race. Together, these amendments transformed the relationship between the federal government and individual rights, making the federal government the primary protector of civil rights."),

    (2, "Bureaucracy", "hard",
     "How does the concept of 'administrative discretion' relate to the debate over bureaucratic accountability?",
     "Administrative discretion refers to the latitude agencies have in implementing laws; critics argue it gives unelected officials too much power, while supporters argue it is necessary for effective governance.",
     json.dumps(["Administrative discretion means agencies must follow congressional instructions word-for-word with no flexibility.",
                  "Administrative discretion was eliminated by the Supreme Court and no longer exists.",
                  "Administrative discretion applies only to the judicial branch, not to executive agencies."]),
     "Administrative discretion is the authority that Congress delegates to administrative agencies to make decisions within broad statutory guidelines. For example, the Environmental Protection Agency has discretion to determine safe levels of pollutants, and the Federal Communications Commission has discretion to allocate radio frequencies. Critics argue that this gives unelected bureaucrats quasi-legislative power without democratic accountability — the 'administrative state' problem. Supporters argue that Congress lacks the expertise to make detailed technical decisions and that discretion is necessary for responsive, effective governance."),

    (2, "State and local government", "hard",
     "How do 'general law' and 'charter' forms of local government differ, and what is the significance of home rule?",
     "General law cities operate under state law with limited authority; charter cities have their own constitutions (charters) granting broader self-governing authority under home rule.",
     json.dumps(["General law cities have complete autonomy; charter cities are directly controlled by the state legislature.",
                  "There is no difference between general law and charter cities — both operate identically.",
                  "Charter cities are illegal under the Constitution and cannot exist."]),
     "The distinction between general law and charter cities reflects the continuum of local government autonomy. General law cities operate under standardized state laws that define their structure and powers — they can only exercise powers that the state has specifically granted. Charter cities, by contrast, adopt their own local constitution (charter) that defines their governmental structure, powers, and procedures. Charter cities operate under home rule, meaning they can act on matters of local concern unless the state has specifically prohibited that action. About half of American cities operate under charters, giving them significantly more autonomy than general law cities."),

    # D3 — 7 more
    (3, "Federalist vs Anti-Federalist debate", "medium",
     "What was Cato's Letters and how did they influence American revolutionary thought?",
     "Cato's Letters were essays by John Trenchard and Thomas Gordon (1720-1723) criticizing corruption and tyranny in British government; they were widely read in the colonies and influenced revolutionary ideology.",
     json.dumps(["Cato's Letters were love letters between Benjamin Franklin and his wife.",
                  "Cato's Letters were official British government documents outlining colonial policy.",
                  "Cato's Letters were written by the Roman emperor Cato in ancient times."]),
     "Cato's Letters, a series of essays by British writers John Trenchard and Thomas Gordon published between 1720 and 1723, were among the most widely read political works in colonial America. Writing under the pseudonym 'Cato' (after the Roman statesman known for opposing tyranny), they criticized political corruption, the abuse of executive power, and the violation of civil liberties. Their ideas about liberty, government accountability, and the right to resist tyranny deeply influenced American revolutionary thought. They were frequently cited by the Founders and were a direct intellectual ancestor of the Anti-Federalist movement."),

    (3, "Federalist vs Anti-Federalist debate", "hard",
     "What were the Centinel essays, and what primary concern did they express about the Constitution?",
     "Written by Anti-Federalist Samuel Bryan under the pseudonym 'Centinel,' they warned that the large republic created by the Constitution would be too distant from the people to represent their interests.",
     json.dumps(["The Centinel essays were Federalist papers supporting the Constitution without reservation.",
                  "The Centinel essays were about agricultural policy and had nothing to do with the Constitution.",
                  "The Centinel essays argued that the Constitution should give more power to the President."]),
     "The Centinel essays, published in Philadelphia newspapers in 1787-88, were among the most influential Anti-Federalist writings. Written by Samuel Bryan under the pseudonym 'Centinel,' they argued that the proposed Constitution would create a government too large and distant to be responsive to ordinary citizens. Centinel warned that the necessary and proper clause and the supremacy clause would allow the federal government to swallow state sovereignty. The essays also expressed concern that the President's power as Commander in Chief could lead to military dictatorship. These arguments directly prompted Federalist responses and influenced the ratification debate."),

    (3, "Declaration of Independence", "hard",
     "How did the concept of 'self-evident truths' in the Declaration reflect Enlightenment philosophy?",
     "The idea that certain truths are self-evident — requiring no proof because they are obvious to any rational person — reflects the Enlightenment belief in reason as the primary source of knowledge and authority.",
     json.dumps(["Self-evident truths was a religious concept with no connection to Enlightenment philosophy.",
                  "The phrase 'self-evident truths' was added by a committee and was not part of Jefferson's original draft.",
                  "Self-evident truths was a medieval concept that the Founders accidentally included."]),
     "Jefferson's opening that 'We hold these truths to be self-evident' is a direct application of Enlightenment epistemology — the theory of knowledge. The Enlightenment, particularly the work of John Locke, held that certain truths could be known through reason alone, without the need for empirical proof or religious authority. By declaring these truths 'self-evident,' Jefferson was making a radical epistemological claim: the principles of equality and unalienable rights are not granted by governments, kings, or churches — they are inherent truths that any rational person can recognize. This was a direct challenge to the divine right of kings and the authority of tradition."),

    (3, "Constitutional Convention", "hard",
     "What was the 'Connecticut Compromise' on the presidency, and how did it resolve the debate over executive selection?",
     "The Convention compromised between legislative election of the President (favored by some) and direct popular election (favored by others) by creating the Electoral College as a compromise mechanism.",
     json.dumps(["The Convention decided that the President should be elected by the Supreme Court.",
                  "There was no debate about how to select the President; all delegates agreed on direct popular vote from the start.",
                  "The Convention created a monarchy with the President serving for life."]),
     "The method for selecting the President was one of the most contentious issues at the Constitutional Convention. Delegates debated several options: election by Congress (feared as creating undue legislative influence over the executive), direct popular election (feared as giving too much power to uneducated voters), election by state governors, and election by electors. The Electoral College was the final compromise — state-appointed electors would vote for President, with each state's electors equal to its congressional delegation. The Framers expected electors to exercise independent judgment, though the system quickly evolved into one where electors are expected to vote for their party's candidate."),

    (3, "English constitutional heritage", "hard",
     "How did John Locke's theory of property rights influence the American Revolution and the Constitution?",
     "Locke argued that property rights arise from mixing labor with natural resources, that governments exist primarily to protect property, and that taxation without consent violates property rights — directly influencing revolutionary ideology.",
     json.dumps(["Locke argued that property should be abolished and all resources shared equally.",
                  "Locke had no theory of property rights; this concept was invented by Karl Marx.",
                  "Locke's property theory was rejected by the American Founders as impractical."]),
     "Locke's theory of property rights was perhaps his most direct influence on the American Revolution. In Chapter V of the Second Treatise, Locke argued that individuals acquire property rights by mixing their labor with natural resources — a person who clears land or builds something owns it because they have invested their labor. This theory made property a natural right, not a government grant. Locke also argued that government's primary purpose is to protect property (broadly defined to include life and liberty). His argument that taxation without representation violates property rights directly influenced the revolutionary slogan 'no taxation without representation' and the Fifth Amendment's Takings Clause."),

    (3, "Founding era", "medium",
     "What was the significance of Thomas Paine's Common Sense (1776)?",
     "It was a bestselling pamphlet that argued for American independence in plain, accessible language, convincing many ordinary colonists that independence was necessary and achievable.",
     json.dumps(["It was a legal document filed in British court arguing for colonial representation in Parliament.",
                  "It was a private letter from Thomas Paine to George Washington that was never published.",
                  "It argued against American independence and urged reconciliation with Britain."]),
     "Thomas Paine's Common Sense, published in January 1776, was the most influential political pamphlet of the American Revolution. Written in clear, forceful prose accessible to ordinary readers, it attacked the institution of monarchy, argued that the American colonies had no economic or political reason to remain tied to Britain, and called for immediate declaration of independence. It sold an estimated 500,000 copies in a colonies of 2.5 million people, making it the best-selling American work of the 18th century. Common Sense shifted public opinion dramatically — before its publication, most colonists sought reconciliation with Britain; after it, independence became the majority position."),

    (3, "Founding era", "medium",
     "What was the Articles of Confederation's greatest achievement, and what was its fatal flaw?",
     "Its greatest achievement was winning the Revolutionary War and creating the Northwest Ordinance; its fatal flaw was the inability to tax or enforce laws, making the national government powerless.",
     json.dumps(["Its greatest achievement was establishing a strong military; its fatal flaw was creating too many courts.",
                  "Its greatest achievement was establishing free trade with Britain; its fatal flaw was that it was too powerful.",
                  "It had no achievements and its only flaw was that it was written too recently."]),
     "The Articles of Confederation's greatest achievement was providing the framework for the United States to win the Revolutionary War and negotiate the Treaty of Paris (1783). It also achieved the Northwest Ordinance (1787), which established the process for admitting new states and banning slavery in the Northwest Territory. However, its fatal flaw was structural: the national government could not tax, could not regulate commerce, could not enforce its laws, and required unanimous consent for amendments. Shays' Rebellion (1786-87) exposed these weaknesses so dramatically that even many who had benefited from the weak national government agreed that a stronger framework was necessary."),
]

conn = sqlite3.connect(DB)
cur = conn.cursor()
for q in questions:
    cur.execute(
        "INSERT INTO questions (fcle_domain, topic, difficulty, question, correct_answer, wrong_answers, explanation) VALUES (?,?,?,?,?,?,?)",
        q
    )
conn.commit()
print(f"Inserted {len(questions)} questions (D2: 4, D3: 7)")
conn.close()
