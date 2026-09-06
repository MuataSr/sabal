#!/usr/bin/env python3
"""Add D3 questions: deeper coverage of founding documents, Enlightenment philosophy, English heritage."""
import sqlite3, json

DB = "fcle.db"

questions = [
    # Enlightenment philosophy (5)
    (3, "Enlightenment philosophy", "easy",
     "Which Enlightenment philosopher most directly influenced the Declaration of Independence's assertion of natural rights?",
     "John Locke, who argued that all people possess natural rights to life, liberty, and property.",
     json.dumps(["Thomas Hobbes, who argued that strong authoritarian government was necessary to prevent chaos.",
                  "Jean-Jacques Rousseau, who argued that direct democracy was the only legitimate form of government.",
                  "Niccolò Machiavelli, who argued that political leaders should use any means necessary to maintain power."]),
     "John Locke's Two Treatises of Government (1689) was the single most influential work on the American Founding. Locke argued that in the state of nature, all people possess natural rights to life, liberty, and property. Governments are formed by social contract to protect these rights, and when governments fail to do so, the people have the right to alter or abolish them. Thomas Jefferson adapted Locke's natural rights theory in the Declaration of Independence, replacing 'property' with 'the pursuit of happiness.'"),

    (3, "Enlightenment philosophy", "medium",
     "How did Thomas Hobbes's and John Locke's views on the state of nature differ, and which view did the Founders adopt?",
     "Hobbes saw the state of nature as violent chaos requiring a strong ruler; Locke saw it as generally peaceful with natural rights. The Founders adopted Locke's view.",
     json.dumps(["Both Hobbes and Locke viewed the state of nature identically; the Founders adopted both views equally.",
                  "Hobbes saw the state of nature as peaceful; Locke saw it as violent. The Founders adopted Hobbes's view.",
                  "Neither philosopher discussed the state of nature; this concept originated with the American Founders."]),
     "In Leviathan (1651), Thomas Hobbes described the state of nature as a 'war of every man against every man' where life was 'solitary, poor, nasty, brutish, and short.' He argued people must surrender their rights to an absolute sovereign in exchange for security. Locke, by contrast, described the state of nature as a condition of freedom and equality governed by natural law. The American Founders overwhelmingly adopted Locke's view, which supported limited government that protects natural rights rather than Hobbes's authoritarian model."),

    (3, "Enlightenment philosophy", "medium",
     "How did Montesquieu's Spirit of the Laws influence the structure of the U.S. Constitution?",
     "Montesquieu argued that liberty is best preserved by separating government into legislative, executive, and judicial branches — the model adopted by the Constitution.",
     json.dumps(["Montesquieu argued that a single all-powerful legislature was the best form of government.",
                  "Montesquieu's work had no significant influence on the Constitution; it was based entirely on English common law.",
                  "Montesquieu advocated for a theocratic government structure based on religious principles."]),
     "Baron de Montesquieu's Spirit of the Laws (1748) argued that political liberty requires the separation of governmental powers into distinct branches that can check each other. He cited the British system as an example, though the British system actually blends legislative and executive power. The Framers adopted Montesquieu's concept more faithfully than the British model itself, creating three genuinely separate branches (Articles I, II, and III) with checks and balances. James Madison cited Montesquieu repeatedly in the Federalist Papers."),

    (3, "Enlightenment philosophy", "hard",
     "What is the concept of 'consent of the governed' and how did it challenge the prevailing political theory of the 18th century?",
     "Consent of the governed holds that legitimate government authority comes from the people, not from divine right or heredity — directly challenging the divine right of kings.",
     json.dumps(["Consent of the governed means that only the King's advisors must approve laws before they take effect.",
                  "Consent of the governed was a traditional English principle that had been accepted since the Magna Carta without controversy.",
                  "Consent of the governed means that all laws must be approved by a majority of world governments."]),
     "The concept of consent of the governed, articulated most clearly by Locke, holds that government derives its just powers from the consent of the people it governs. This directly challenged the prevailing European doctrine of the divine right of kings, which held that monarchs received their authority directly from God and were not accountable to their subjects. The Declaration of Independence opens with this principle: 'Governments are instituted among Men, deriving their just powers from the consent of the governed.' This was revolutionary for its time."),

    (3, "Enlightenment philosophy", "easy",
     "What is 'natural law' in the context of Enlightenment political philosophy?",
     "A universal moral law that exists independently of human legislation and can be discovered through reason.",
     json.dumps(["A set of laws passed by Parliament that apply to all British colonies.",
                  "Laws that are written into the U.S. Constitution's first ten amendments.",
                  "Laws that are created by scientists to explain the natural world."]),
     "Natural law is the philosophical concept that there exists a universal moral law inherent in nature that can be understood through human reason. Enlightenment thinkers like Locke argued that natural law grants all people fundamental rights (life, liberty, property) that no government can legitimately take away. This concept influenced both the Declaration of Independence and the Constitution. Natural law theory holds that human-made (positive) law is only legitimate when it conforms to these higher moral principles."),

    # Declaration of Independence — deeper (5)
    (3, "Declaration of Independence", "medium",
     "What are the three main sections of the Declaration of Independence?",
     "A statement of natural rights and the purpose of government, a list of grievances against King George III, and a formal declaration of independence.",
     json.dumps(["A description of British tax policy, a list of military victories, and a peace treaty proposal.",
                  "An explanation of federalism, a list of amendments proposed for the Constitution, and a bill of rights.",
                  "A preamble, the Articles of Confederation, and the Treaty of Paris."]),
     "The Declaration of Independence has three main sections. First, it articulates the philosophical foundation: that all people have unalienable rights, that governments exist to protect those rights, and that people have the right to alter or abolish governments that fail to protect them. Second, it lists 27 specific grievances against King George III, justifying the decision to declare independence. Third, it formally declares that the colonies are free and independent states with full power to govern themselves."),

    (3, "Declaration of Independence", "medium",
     "According to the Declaration of Independence, what is the primary purpose of government?",
     "To secure the unalienable rights of life, liberty, and the pursuit of happiness.",
     json.dumps(["To enforce laws and collect taxes from citizens.",
                  "To expand territory and increase national power.",
                  "To establish a official religion and promote moral virtue."]),
     "The Declaration states that governments are instituted 'to secure these rights' — referring to the unalienable rights of life, liberty, and the pursuit of happiness. This is a profoundly limited view of government purpose. Government exists not to grant rights (which are inherent) but to protect them. When a government becomes 'destructive of these ends,' the Declaration argues, 'it is the Right of the People to alter or to abolish it, and to institute new Government.' This idea fundamentally shaped American political thought."),

    (3, "Declaration of Independence", "hard",
     "Why did the Declaration of Independence list 27 grievances against King George III rather than against Parliament?",
     "The colonists wanted to frame their dispute as a violation of the social contract by the King, arguing that the King had failed in his duty to protect their rights.",
     json.dumps(["The colonists believed Parliament did not exist and was a fictional body created by British propaganda.",
                  "The colonists were actually loyal to Parliament and blamed only the King for their problems.",
                  "The Declaration does not list grievances against anyone; it is entirely a philosophical document."]),
     "The Declaration's list of grievances was carefully directed at King George III for strategic and philosophical reasons. By blaming the King, the colonists framed their argument as a breach of the social contract — the monarch had failed his duty to protect his subjects' natural rights. This avoided the more complex constitutional argument about Parliament's authority over the colonies. It also aligned with the Declaration's philosophical framework (Locke's right of revolution), which holds that people may overthrow a tyrant who violates the trust of governance."),

    (3, "Declaration of Independence", "easy",
     "Who was the primary author of the Declaration of Independence?",
     "Thomas Jefferson.",
     json.dumps(["Benjamin Franklin",
                  "John Adams",
                  "George Washington"]),
     "Thomas Jefferson, then 33 years old, was the principal author of the Declaration of Independence. He was appointed to a five-member Committee of Five (also including John Adams, Benjamin Franklin, Roger Sherman, and Robert Livingston) by the Second Continental Congress. Jefferson wrote the first draft, which was revised by the committee and then further edited by the full Congress before adoption on July 4, 1776. Jefferson's draft included a passage condemning slavery that was removed to secure support from Southern delegates."),

    (3, "Declaration of Independence", "medium",
     "Why was the Declaration of Independence primarily a political document rather than a legal document?",
     "It declared independence and justified it philosophically, but it created no binding legal obligations or government structure.",
     json.dumps(["It was declared illegal by the British government and therefore had no legal standing.",
                  "It was a legal contract between the colonies and the King that could be enforced in British courts.",
                  "It was both a legal and political document with equal weight in both domains."]),
     "The Declaration of Independence is a foundational political document, not a legal one. It did not create a government, establish laws, or define legal procedures. Its purpose was to announce the colonies' decision to separate from Britain and to justify that decision through natural rights philosophy. The legal framework for American government came later with the Articles of Confederation (1781) and then the Constitution (1789). However, the Declaration's principles — especially equality and unalienable rights — have profoundly influenced American constitutional law and legal interpretation."),

    # English constitutional heritage (5)
    (3, "English constitutional heritage", "medium",
     "How did the Magna Carta (1215) influence American constitutional law?",
     "The Magna Carta established the principle that even the king is subject to the law, introducing concepts of due process and limited government that influenced the U.S. Constitution.",
     json.dumps(["The Magna Carta was a French document that had no influence on American law.",
                  "The Magna Carta established the principle that kings have absolute power over their subjects.",
                  "The Magna Carta was the first document to create a democratic parliament."]),
     "The Magna Carta (Great Charter) of 1215, forced upon King John by rebellious barons, is one of the most important ancestors of American constitutional law. It established the principle of rule of law — that even the sovereign is subject to legal constraints. Key provisions influenced the Fifth Amendment's due process clause ('no person shall be deprived of life, liberty, or property without due process of law') and the Sixth Amendment's right to a jury trial. The Magna Carta's legacy is the idea that government power has limits."),

    (3, "English constitutional heritage", "medium",
     "How did the English Bill of Rights (1689) influence the American Bill of Rights?",
     "The English Bill of Rights established specific protections (free speech in Parliament, protection against excessive bail, right to petition) that were adapted into the U.S. Bill of Rights.",
     json.dumps(["The American Bill of Rights was copied word-for-word from the English Bill of Rights with no changes.",
                  "The English Bill of Rights had no influence because it was written after the American Bill of Rights.",
                  "The English Bill of Rights established only economic rights, not civil liberties."]),
     "The English Bill of Rights of 1689 directly influenced the American Bill of Rights. The English document guaranteed free elections, freedom of speech in Parliament, protection against excessive bail and cruel punishment, and the right to petition the monarch. The American Founders adapted these protections: the Eighth Amendment's prohibition on excessive bail and cruel punishment, the First Amendment's right to petition, and the First Amendment's freedom of speech all trace their lineage to the English Bill of Rights."),

    (3, "English constitutional heritage", "hard",
     "What was the significance of the Petition of Right (1628) in the development of English and American constitutional principles?",
     "The Petition of Right asserted that the King could not tax without Parliament's consent, imprison without cause, quarter soldiers in private homes, or impose martial law in peacetime.",
     json.dumps(["The Petition of Right granted the King unlimited power to tax and imprison subjects during wartime.",
                  "The Petition of Right established that Parliament had no authority over the King's decisions.",
                  "The Petition of Right was a religious document that established the Church of England's supremacy."]),
     "The Petition of Right (1628) was passed by Parliament under Charles I and is a direct ancestor of several constitutional protections. It asserted four key principles: no taxation without Parliament's consent (influencing 'no taxation without representation'), no imprisonment without cause (influencing the Fifth Amendment's due process), no quartering of soldiers in private homes (directly adopted in the Third Amendment), and no martial law in peacetime. These principles became foundational to American constitutional thought."),

    (3, "English constitutional heritage", "easy",
     "What principle from English constitutional history is reflected in the Third Amendment of the U.S. Constitution?",
     "The prohibition on quartering soldiers in private homes, originating from the Petition of Right (1628) and reinforced by the English Bill of Rights (1689).",
     json.dumps(["The right to a trial by jury, originating from the Magna Carta.",
                  "The prohibition on excessive bail, originating from English common law.",
                  "The right to free speech, originating from the Glorious Revolution."]),
     "The Third Amendment — 'No Soldier shall, in time of peace be quartered in any house, without the consent of the Owner, nor in time of war, but in a manner to be prescribed by law' — directly traces its origins to English constitutional history. The Petition of Right (1628) and the English Bill of Rights (1689) both prohibited the quartering of soldiers in private homes without consent. This was a significant grievance against the British during the American Revolution, as British forces routinely quartered troops in colonial homes."),

    (3, "English constitutional heritage", "medium",
     "How did the concept of 'no taxation without representation' develop from English constitutional history?",
     "It evolved from the principle established in the Magna Carta and Petition of Right that taxation requires the consent of those being taxed, which the colonists argued Parliament violated.",
     json.dumps(["It was invented by American colonists in 1765 and had no prior history in English law.",
                  "It was a British principle that Parliament followed strictly and the colonists rejected.",
                  "It originated from French revolutionary philosophy and was imported to America by Thomas Jefferson."]),
     "The principle of 'no taxation without representation' has deep roots in English constitutional history. The Magna Carta (1215) established that taxation required consent. The Petition of Right (1628) explicitly stated that taxation without Parliament's consent was illegal. When Parliament began taxing the American colonies (Stamp Act 1765, Townshend Acts 1767), the colonists argued they had no representation in Parliament and therefore could not be constitutionally taxed. This was not a new principle — the colonists were appealing to established English constitutional traditions."),

    # Federalist vs Anti-Federalist deeper (5)
    (3, "Federalist vs Anti-Federalist debate", "hard",
     "What was the Anti-Federalists' strongest argument against ratification of the Constitution, and how was it addressed?",
     "The Constitution lacked a Bill of Rights to protect individual liberties from federal power; this was addressed by adding the first ten amendments.",
     json.dumps(["The Constitution gave too much power to the judiciary; this was addressed by reducing the number of Supreme Court justices.",
                  "The Constitution abolished state governments entirely; this was addressed by the Tenth Amendment.",
                  "The Constitution allowed the President to serve for life; this was addressed by the Twenty-Second Amendment."]),
     "The Anti-Federalists' most powerful and ultimately most successful argument was that the Constitution needed a Bill of Rights to protect individual liberties against federal power. Federalists initially argued a Bill of Rights was unnecessary because the federal government had only delegated powers. But Anti-Federalists, led by George Mason and Patrick Henry, insisted that without explicit protections, the government could eventually exceed its delegated powers. This argument carried the day: several states ratified only on the promise of amendments, and the Bill of Rights was added in 1791."),

    (3, "Federalist vs Anti-Federalist debate", "medium",
     "What was the Federalists' response to the Anti-Federalist concern that a strong central government would threaten liberty?",
     "Federalists argued that the Constitution's system of separation of powers, checks and balances, and federalism would prevent any single group from dominating.",
     json.dumps(["Federalists agreed that the central government would be too powerful and proposed weakening it significantly.",
                  "Federalists argued that individual liberty was less important than national security.",
                  "Federalists responded that no government could ever threaten liberty because the people could always revolt."]),
     "Federalists responded to Anti-Federalist concerns by pointing to the Constitution's structural safeguards against tyranny. In Federalist No. 51, Madison argued that 'ambition must be made to counteract ambition' through the system of checks and balances. Federalism provided a 'double security' — power divided between federal and state governments, and within the federal government divided among three branches. The large republic argument (Federalist No. 10) also addressed this concern by showing that a diverse republic would prevent any single faction from dominating."),

    (3, "Federalist vs Anti-Federalist debate", "easy",
     "Who were the Anti-Federalists?",
     "Opponents of the Constitution who feared it created an overly powerful central government at the expense of states and individual rights.",
     json.dumps(["Supporters of a strong federal government who wrote the Federalist Papers.",
                  "Members of a political party that opposed all forms of government.",
                  "Foreign diplomats who interfered in the American ratification process."]),
     "Anti-Federalists were a diverse coalition of Americans who opposed ratification of the Constitution in 1787-88. Key figures included Patrick Henry ('Give me liberty or give me death!'), George Mason (author of the Virginia Declaration of Rights), and Richard Henry Lee. They feared the Constitution centralized too much power, lacked protections for individual rights, threatened state sovereignty, and would create an aristocratic government distant from ordinary citizens. Though they lost the ratification debate, they won the Bill of Rights."),

    (3, "Federalist vs Anti-Federalist debate", "medium",
     "What was the significance of The Federalist Papers in the ratification debate?",
     "The Federalist Papers provided systematic arguments for the Constitution, explaining its structure and defending it against Anti-Federalist criticism, and remain a key source for constitutional interpretation.",
     json.dumps(["The Federalist Papers were Anti-Federalist essays that successfully convinced states to reject the Constitution.",
                  "The Federalist Papers had little impact on ratification because most people could not read them.",
                  "The Federalist Papers were written after the Constitution was already ratified and had no effect on the debate."]),
     "The Federalist Papers (1787-88), written by Alexander Hamilton, James Madison, and John Jay under the pseudonym 'Publius,' were 85 essays published in New York newspapers to persuade that state to ratify the Constitution. While their immediate impact on ratification is debated (New York ratified narrowly), their long-term significance is enormous. They remain the most authoritative explanation of the Constitution's design and are routinely cited by Supreme Court justices interpreting constitutional provisions, particularly Federalist No. 10 (factions) and No. 51 (separation of powers)."),

    (3, "Federalist vs Anti-Federalist debate", "hard",
     "What were the Brutus essays, and what concern did they raise that Federalist No. 78 attempted to address?",
     "The Brutus essays were Anti-Federalist writings warning that the federal judiciary would become too powerful; Federalist No. 78 argued that the judiciary would be the 'least dangerous' branch.",
     json.dumps(["The Brutus essays supported a stronger judiciary; Federalist No. 78 argued for weakening it.",
                  "The Brutus essays were Federalist papers; Federalist No. 78 was an Anti-Federalist response.",
                  "The Brutus essays concerned the military; Federalist No. 78 addressed economic policy."]),
     "The Brutus essays, written by an anonymous Anti-Federalist (likely Robert Yates, a New York judge), warned that the federal judiciary created by the Constitution would become the most powerful branch, able to strike down state laws and interpret the Constitution to expand federal power. In Federalist No. 78, Hamilton responded that the judiciary would be the 'least dangerous branch' because it has 'no influence over either the sword or the purse.' This debate remains relevant today as the Supreme Court's power of judicial review continues to be a central feature of American governance."),
]

conn = sqlite3.connect(DB)
cur = conn.cursor()
for q in questions:
    cur.execute(
        "INSERT INTO questions (fcle_domain, topic, difficulty, question, correct_answer, wrong_answers, explanation) VALUES (?,?,?,?,?,?,?)",
        q
    )
conn.commit()
print(f"Inserted {len(questions)} D3 questions")
conn.close()
