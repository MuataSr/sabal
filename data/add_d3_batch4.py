#!/usr/bin/env python3
"""Add D3 questions batch 4: 30 more (heavy on hard) to reach 150."""
import sqlite3, json

DB = "fcle.db"

questions = [
    # Hard: Enlightenment and philosophy (8)
    (3, "Enlightenment philosophy", "hard",
     "How did Jean-Jacques Rousseau's concept of the 'general will' differ from Locke's conception of government by consent?",
     "Rousseau argued that the general will — the collective interest of all citizens — is sovereign and cannot be represented, while Locke focused on protecting individual natural rights through representative government.",
     json.dumps(["Rousseau and Locke had identical views on government; there is no meaningful difference.",
                  "Rousseau opposed all forms of government, while Locke supported absolute monarchy.",
                  "Rousseau's general will refers to military strategy, while Locke's consent refers to economic policy."]),
     "Rousseau's 'general will' (le volonté générale), articulated in The Social Contract (1762), differs fundamentally from Locke's consent theory. For Rousseau, the general will is the collective interest of the citizen body as a whole — it is indivisible and cannot be delegated to representatives. Citizens must participate directly in lawmaking. Locke, by contrast, envisioned a representative government that protects pre-existing individual rights (life, liberty, property). Rousseau's ideas influenced the French Revolution more than the American, though his emphasis on popular sovereignty resonated with some American democratic principles."),

    (3, "Enlightenment philosophy", "hard",
     "What was the 'social contract' theory, and how did different Enlightenment philosophers conceive of it differently?",
     "The social contract theory holds that government legitimacy derives from an agreement among the people; Hobbes saw it as surrendering rights to a sovereign, Locke as protecting natural rights, and Rousseau as expressing the general will.",
     json.dumps(["All social contract theorists agreed on a single unified theory of government with no differences.",
                  "Social contract theory was rejected by all Enlightenment philosophers as unrealistic.",
                  "Social contract theory argues that government exists independently of any agreement with the people."]),
     "Social contract theory holds that legitimate political authority derives from a contract or agreement among individuals, not from divine right or force. Three major Enlightenment philosophers developed distinct versions. Thomas Hobbes (Leviathan, 1651) argued that people surrender all rights to an absolute sovereign in exchange for security from the violent state of nature. John Locke (Two Treatises, 1689) argued that people retain natural rights and establish limited government to protect them. Rousseau (Social Contract, 1762) argued that the contract creates a community governed by the general will. These three versions represent a spectrum from authoritarian to democratic."),

    (3, "Enlightenment philosophy", "hard",
     "How did the concept of 'unalienable rights' in the Declaration of Independence draw on both Enlightenment philosophy and English constitutional tradition?",
     "It combined Locke's natural rights theory (rights inherent in all people by nature) with the English tradition of recognized liberties (Magna Carta, Petition of Right, Bill of Rights) to create a uniquely American synthesis.",
     json.dumps(["The concept was entirely original to Jefferson with no intellectual antecedents.",
                  "The concept was borrowed directly from French revolutionary documents with no English influence.",
                  "The concept was created by the British monarchy and imposed on the colonies."]),
     "The concept of 'unalienable rights' in the Declaration of Independence represents a synthesis of multiple intellectual traditions. From Locke and Enlightenment philosophy came the idea that rights exist by nature, independent of government — life, liberty, and property (Jefferson modified this to 'pursuit of happiness'). From English constitutional tradition came the specific rights that had been recognized over centuries: the Magna Carta's due process, the Petition of Right's limits on arbitrary power, and the English Bill of Rights' protections for speech, petition, and trial rights. Jefferson fused these traditions into a universal claim about human rights."),

    (3, "Enlightenment philosophy", "hard",
     "What is the 'state of nature' concept in political philosophy, and why was it important to the American Founding?",
     "The state of nature is a hypothetical condition of humanity before government; it was used by Enlightenment philosophers to derive the purpose and limits of government through natural law.",
     json.dumps(["The state of nature refers to the environmental movement and its influence on conservation policy.",
                  "The state of nature was a concept used exclusively by European monarchs to justify absolute power.",
                  "The state of nature has no connection to political philosophy or the American Founding."]),
     "The 'state of nature' is a thought experiment used by social contract theorists to imagine what human life would be like without government. For Hobbes, it was a violent war of all against all, justifying strong authoritarian rule. For Locke, it was a condition of freedom and equality governed by natural law, where people had natural rights but lacked impartial judges to settle disputes — justifying limited government to protect those rights. This concept was crucial to the American Founding because it established that government exists to serve the people (not vice versa) and that legitimate government is based on the consent of the governed, not divine right."),

    (3, "Enlightenment philosophy", "hard",
     "How did Adam Smith's economic philosophy influence the American Founding?",
     "Smith's argument for free markets and limited government economic intervention influenced the Constitution's Commerce Clause and the Founders' preference for a national free-trade area.",
     json.dumps(["Smith's philosophy was unknown to the American Founders and had no influence on the Constitution.",
                  "Smith advocated for complete government control of the economy, which the Founders adopted.",
                  "Smith's philosophy applied only to agriculture and had no relevance to the American economy."]),
     "Adam Smith's Wealth of Nations (1776) was published the same year as American independence and significantly influenced the Founders' economic thinking. Smith argued that free trade, division of labor, and limited government intervention create national prosperity. This influenced several constitutional provisions: the Commerce Clause (giving Congress power to regulate interstate commerce and prevent state trade barriers), the prohibition on states coining money or impairing contracts, and the general preference for a national free-trade area. Alexander Hamilton, though not a free-market purist, drew on Smith's ideas in his economic reports as Treasury Secretary."),

    (3, "Enlightenment philosophy", "hard",
     "What role did the concept of 'virtue' play in the Founders' political philosophy?",
     "The Founders believed that republican government required civic virtue — citizens willing to put the public good above private interest — and feared that corruption and factionalism would destroy the republic.",
     json.dumps(["The Founders rejected the concept of virtue as irrelevant to government, focusing only on institutional design.",
                  "The Founders believed virtue was automatically guaranteed by the Constitution's structure.",
                  "Virtue was a concept from Greek philosophy that the Founders explicitly rejected."]),
     "Civic virtue — the willingness of citizens to sacrifice personal interest for the public good — was central to the Founders' political thought. They believed republican government could not survive without a virtuous citizenry. Washington repeatedly warned against the corrupting influence of factionalism and self-interest. Jefferson believed education was essential for cultivating civic virtue. Madison designed the Constitution's checks and balances partly as a supplement to virtue, acknowledging that 'if men were angels, no government would be necessary.' The tension between relying on virtue and designing institutions to work despite its absence is a central theme of American constitutional design."),

    # Hard: Federalist Papers deeper (5)
    (3, "Federalist Papers", "hard",
     "What was the argument in Federalist No. 10 about factions, and how did Madison propose to control their effects?",
     "Madison defined factions as groups united by a common interest adverse to others; he argued a large republic with diverse interests would prevent any single faction from dominating.",
     json.dumps(["Madison argued that factions should be completely eliminated through strict government censorship.",
                  "Madison argued that factions were beneficial and should be given maximum political power.",
                  "Madison argued that the Constitution could not address factions and they should simply be ignored."]),
     "Federalist No. 10, considered Madison's most important contribution to political theory, addresses the problem of factions — groups of citizens 'united and actuated by some common impulse of passion, or of interest, adverse to the rights of other citizens, or to the permanent and aggregate interests of the community.' Madison argued that eliminating factions would destroy liberty, so the solution was to control their effects. In a large republic with many diverse interests, no single faction could become a majority. This 'extended sphere' argument was Madison's key innovation — it turned the size of the nation from a weakness (as under the Articles) into a strength."),

    (3, "Federalist Papers", "hard",
     "How does Federalist No. 51 explain the system of checks and balances, and what famous phrase does it contain?",
     "Federalist No. 51 explains that ambition counteracts ambition through the separation of powers, containing the famous phrase 'If men were angels, no government would be necessary.'",
     json.dumps(["Federalist No. 51 argues that a single all-powerful branch is the most effective form of government.",
                  "Federalist No. 51 contains the phrase 'all men are created equal,' which was later used in the Declaration of Independence.",
                  "Federalist No. 51 argues that the judiciary should be the strongest branch of government."]),
     "Federalist No. 51, Madison's companion to No. 10, explains the structural design of the Constitution. Its most famous passage: 'If men were angels, no government would be necessary. If angels were to govern men, neither external nor internal controls on government would be necessary.' Madison argues that since people are not angels, government is necessary, and since those who govern are not angels either, controls on government are equally necessary. The solution: 'ambition must be made to counteract ambition' by giving each branch 'the necessary constitutional means and personal motives to resist encroachments of the others.' This elegant theory explains the entire system of checks and balances."),

    (3, "Federalist Papers", "hard",
     "What is the 'double security' argument in Federalist No. 51 regarding federalism?",
     "Federalism provides double protection for liberty by dividing power between federal and state governments — different levels of government will check each other as well as separate branches checking each other.",
     json.dumps(["Double security refers to requiring two branches to approve every law before it takes effect.",
                  "Double security means every citizen has two votes in every election.",
                  "Double security refers to the President's ability to veto any congressional action twice."]),
     "Federalist No. 51 argues that federalism creates a 'double security' for the rights of the people. Power is divided first between federal and state governments, and then within the federal government among three branches. 'In the compound republic of America, the power surrendered by the people is first divided between two distinct governments, and then the portion allotted to each subdivided among distinct and separate departments. Hence a double security arises to the rights of the people.' This means the people have two different governments to protect their rights, and each government is internally divided to prevent tyranny within."),

    # Hard: founding documents deeper (8)
    (3, "Declaration of Independence", "hard",
     "How did the Declaration of Independence reconcile the statement 'all men are created equal' with the existence of slavery?",
     "The original draft included a passage condemning the slave trade, but it was removed to secure support from Southern delegates; the tension between the principle and the practice defined American history.",
     json.dumps(["The Declaration explicitly endorsed slavery as consistent with equality.",
                  "The phrase 'all men are created equal' was added after the Civil War and was not in the original document.",
                  "The Founders did not see any conflict between equality and slavery."]),
     "Jefferson's original draft of the Declaration included a passage condemning King George III for perpetuating the slave trade: 'he has waged cruel war against human nature itself, violating its most sacred rights of life and liberty in the persons of a distant people.' This passage was removed after objections from South Carolina and Georgia delegates, who refused to accept any condemnation of slavery. The resulting tension between the Declaration's universal equality principle and the reality of American slavery became a defining contradiction in American history. Frederick Douglass and Abraham Lincoln both used the Declaration's words to argue against slavery."),

    (3, "Constitutional Convention", "hard",
     "What was the Great Compromise (Connecticut Compromise), and why was it essential to the Constitution's success?",
     "The Great Compromise created a bicameral Congress with the House based on population and the Senate with equal state representation, resolving the fundamental conflict between large and small states.",
     json.dumps(["The Great Compromise abolished slavery and freed all enslaved people immediately.",
                  "The Great Compromise gave all power to the federal government and eliminated state sovereignty.",
                  "The Great Compromise was a minor procedural agreement with no significant impact."]),
     "The Great Compromise, proposed by Connecticut delegate Roger Sherman, was the breakthrough that made the Constitution possible. It resolved the fundamental conflict between the Virginia Plan (representation by population, favored by large states) and the New Jersey Plan (equal representation, favored by small states). The compromise created a bicameral Congress: a House of Representatives apportioned by state population (satisfying large states) and a Senate with two members per state regardless of population (satisfying small states). All revenue bills would originate in the House, giving large states some advantage. Without this compromise, the Convention would likely have failed."),

    (3, "Constitutional Convention", "hard",
     "How did the Framers address the issue of slavery at the Constitutional Convention, and what were the three major slavery-related compromises?",
     "The three compromises were the Three-Fifths Compromise (counting enslaved people for representation), the slave trade compromise (banning importation after 1808), and the fugitive slave clause (requiring return of escaped enslaved people).",
     json.dumps(["The Framers completely abolished slavery at the Convention with no compromises.",
                  "The Framers refused to address slavery, leaving it entirely to future generations to resolve.",
                  "The Constitution mentions slavery only once, in a single sentence that has no practical effect."]),
     "The Constitution addressed slavery through three major compromises that reflected the deep divisions between Northern and Southern states. The Three-Fifths Compromise counted enslaved people as three-fifths of a person for representation and taxation. The slave trade compromise prohibited Congress from banning the international slave trade before 1808. The fugitive slave clause (Article IV, Section 2) required that escaped enslaved persons be returned to their enslavers. The word 'slavery' does not appear in the original Constitution — instead, the document uses euphemisms like 'person held to service or labour.' These compromises postponed but did not resolve the slavery question."),

    (3, "Constitutional ratification", "hard",
     "What was the role of state ratifying conventions versus state legislatures in the ratification process, and why was this choice significant?",
     "Ratification by state conventions rather than legislatures ensured that the Constitution reflected the direct will of the people, not just existing political elites.",
     json.dumps(["State legislatures ratified the Constitution unanimously with no conventions involved.",
                  "The Constitution was ratified by a national popular vote with no state involvement.",
                  "Only the President and Supreme Court could ratify constitutional amendments."]),
     "Article VII specified that the Constitution would be ratified by conventions in the states rather than by state legislatures. This was a deliberate choice with profound implications. State legislatures were existing political bodies whose members had been elected under the Articles of Confederation and might resist losing power. Conventions, by contrast, would be specially elected bodies whose sole purpose was to consider the new Constitution. This meant ratification would reflect the direct consent of the people (through their elected delegates) rather than the consent of existing political institutions. It embodied the social contract principle that the people themselves are the source of governmental authority."),

    (3, "Constitutional ratification", "hard",
     "What was the significance of the Federalist-Anti-Federalist debate over standing armies, and how did the Constitution address this concern?",
     "Anti-Federalists feared standing armies as tools of tyranny; the Constitution addressed this by giving Congress (not the President) power to raise armies, limiting appropriations to two years, and trusting civilian control of the military.",
     json.dumps(["Both sides agreed that standing armies should be abolished and replaced with state militias.",
                  "The Constitution gave the President unlimited power to raise and maintain armies without congressional approval.",
                  "Standing armies were not discussed during the ratification debates and are not addressed in the Constitution."]),
     "The fear of standing armies was a major Anti-Federalist concern rooted in English history and colonial experience. British standing armies had been used to enforce unpopular policies in the colonies. Anti-Federalists worried that a national standing army could be used to suppress state governments and individual liberties. The Constitution addressed this by giving Congress (the people's representatives) rather than the President the power to raise and support armies (Article I, Section 8), limiting army appropriations to two years (requiring regular congressional approval), and making the President, a civilian, the Commander in Chief rather than a military officer."),

    # Medium: additional founding era topics (9)
    (3, "Founding era", "medium",
     "Who was James Madison, and what was his role in the creation of the Constitution?",
     "James Madison is known as the 'Father of the Constitution' for his central role in drafting the document, proposing the Virginia Plan, co-authoring the Federalist Papers, and drafting the Bill of Rights.",
     json.dumps(["James Madison was the first President of the United States and led the Revolutionary War.",
                  "James Madison opposed the Constitution and refused to participate in the Constitutional Convention.",
                  "James Madison was a British loyalist who fought against American independence."]),
     "James Madison of Virginia played the central role in creating the Constitution. Before the Convention, he studied government systems extensively and arrived with the Virginia Plan (drafted with Edmund Randolph). During the Convention, he spoke more than any other delegate and kept detailed notes that remain our primary record of the debates. After the Convention, he co-authored the Federalist Papers (writing 29 of 85 essays, including Nos. 10, 51, and the Federalist 39 on federalism). In the First Congress, he drafted the Bill of Rights. He later served as the fourth President (1809-1817)."),

    (3, "Founding era", "medium",
     "What was George Washington's role at the Constitutional Convention?",
     "He presided over the Convention as its president, using his prestige and authority to maintain order and lend credibility to the proceedings.",
     json.dumps(["Washington wrote most of the Constitution himself and dictated its provisions to the delegates.",
                  "Washington opposed the Convention and refused to attend until the final day.",
                  "Washington served as a delegate from New York and argued against creating a stronger national government."]),
     "George Washington was unanimously elected president of the Constitutional Convention. His presence was essential — without the hero of the Revolution presiding, the Convention would have lacked the credibility to propose such fundamental changes to the national government. Washington rarely spoke during debates (only about 150 times over four months), but his influence was enormous. His mere presence kept delegates focused and gave the final product legitimacy. Washington's support for the Constitution after the Convention was the single most important factor in its ratification, as the public trusted him above all other political figures."),

    (3, "Founding era", "medium",
     "What was the significance of the year 1787 in American history?",
     "1787 was the year the Constitutional Convention met in Philadelphia and drafted the U.S. Constitution, replacing the Articles of Confederation.",
     json.dumps(["1787 was the year the Declaration of Independence was signed.",
                  "1787 was the year the Civil War began.",
                  "1787 was the year the Bill of Rights was first proposed and immediately ratified."]),
     "The year 1787 was pivotal in American history. The Constitutional Convention met from May 25 to September 17, 1787, in Philadelphia's Independence Hall. Originally convened to revise the Articles of Confederation, the delegates instead drafted an entirely new frame of government. The same year also saw the Northwest Ordinance passed by the Confederation Congress (establishing the process for admitting new states and banning slavery in the Northwest Territory). Together, the Constitution and the Northwest Ordinance represented the two great achievements of 1787 that shaped the future of the American republic."),

    (3, "Founding era", "medium",
     "What was Benjamin Franklin's role at the Constitutional Convention?",
     "Franklin, at 81 the oldest delegate, served as a unifying figure who proposed the Great Compromise and urged delegates to compromise despite their differences.",
     json.dumps(["Franklin wrote the entire Constitution and forced the other delegates to accept it.",
                  "Franklin was too ill to attend and sent a letter opposing the Constitution.",
                  "Franklin served as a military advisor and had no role in the debates."]),
     "Benjamin Franklin, at 81 years old, was the elder statesman of the Constitutional Convention. His most significant contribution was his speech on June 28, 1787, when the Convention was deadlocked over representation. Franklin urged compromise, acknowledging that he had 'often looked at [the Constitution] with astonishment' and that he did not 'expect from a perfect government perfect happiness,' but that the proposed Constitution was 'astonishingly close to perfection.' He proposed that delegates who still had doubts 'doubt a little of their own infallibility.' His call for compromise helped break the deadlock and paved the way for the Great Compromise."),

    (3, "Founding era", "medium",
     "What was the purpose of the Preamble to the Constitution, and what are its key phrases?",
     "The Preamble states the purposes of the Constitution: to form a more perfect union, establish justice, ensure domestic tranquility, provide for the common defense, promote the general welfare, and secure liberty.",
     json.dumps(["The Preamble is a legal document with binding authority that creates specific government powers.",
                  "The Preamble is a ceremonial introduction with no meaning or significance.",
                  "The Preamble was added in 1791 as part of the Bill of Rights."]),
     "The Preamble begins 'We the People of the United States' and establishes six purposes of the Constitution: (1) form a more perfect Union (improving on the Articles of Confederation), (2) establish Justice (creating fair legal systems), (3) insure domestic Tranquility (maintaining peace and order), (4) provide for the common defence (national security), (5) promote the general Welfare (the well-being of all citizens), and (6) secure the Blessings of Liberty to ourselves and our Posterity. While the Preamble is not itself a source of government power, it establishes the Constitution's purposes and the principle that governmental authority derives from 'the People.'"),

    (3, "Founding era", "medium",
     "Why did the Founders choose a republic rather than a direct democracy?",
     "They believed direct democracy (where citizens vote on every issue) would be impractical in a large nation and would lead to mob rule; a republic with elected representatives would provide stability while reflecting the people's will.",
     json.dumps(["The Founders wanted a direct democracy but were forced to accept a republic by the British government.",
                  "The Founders did not believe in any form of self-government and preferred monarchy.",
                  "Direct democracy and a republic are the same thing with no meaningful distinction."]),
     "The Founders deliberately chose a republic — a system where citizens elect representatives to make laws — rather than a direct democracy, where citizens vote on all laws directly. In Federalist No. 10, Madison argued that direct democracies had historically been 'spectacles of turbulence and contention' and were 'incompatible with personal security or the rights of property.' The Founders also noted that direct democracy was impractical in a nation spanning 1,000 miles. A republic, by contrast, could 'refine and enlarge the public views' through the filter of elected representatives while still deriving its authority from the consent of the governed."),

    (3, "Founding era", "medium",
     "What was the significance of Alexander Hamilton in the founding era?",
     "Hamilton was a leading Federalist, co-author of 51 Federalist Papers, first Secretary of the Treasury, and architect of the early American financial system.",
     json.dumps(["Hamilton was a leading Anti-Federalist who opposed the Constitution and served as Jefferson's Vice President.",
                  "Hamilton was a military general who had no involvement in politics or constitutional design.",
                  "Hamilton was the primary author of the Declaration of Independence."]),
     "Alexander Hamilton was one of the most influential Founders despite never becoming President. He was a leading advocate for the Constitution, writing 51 of the 85 Federalist Papers (more than Madison or Jay). As Washington's first Secretary of the Treasury, Hamilton created the American financial system: establishing a national bank, assuming state Revolutionary War debts, creating a federal tax system, and promoting manufacturing. His financial vision made the United States creditworthy and economically stable. Hamilton's broad interpretation of federal power (contrasted with Jefferson's strict constructionism) established a debate that continues to shape American politics."),

    (3, "Founding era", "medium",
     "What was the Whiskey Rebellion (1794), and what did it demonstrate about the new federal government under the Constitution?",
     "It was a tax protest by Pennsylvania farmers that Washington suppressed with federal troops, demonstrating that the new government could enforce its laws — unlike under the Articles of Confederation.",
     json.dumps(["The Whiskey Rebellion was a peaceful protest that the government resolved through negotiation without force.",
                  "The Whiskey Rebellion proved that the federal government was too weak to maintain order.",
                  "The Whiskey Rebellion was a foreign invasion that the state militias defeated without federal involvement."]),
     "The Whiskey Rebellion (1794) was an armed uprising by western Pennsylvania farmers who opposed Hamilton's excise tax on whiskey, which was their primary medium of exchange. When protesters attacked federal tax collectors, President Washington invoked the Militia Act of 1792 and led a militia force of nearly 13,000 men to suppress the rebellion. The rebels dispersed without a battle. The significance was enormous: under the Articles of Confederation, the federal government could not respond to Shays' Rebellion; under the Constitution, Washington demonstrated that the new federal government had the power to enforce its laws."),

    (3, "Founding era", "medium",
     "What was the significance of the Jay Treaty (1794) for the early republic?",
     "It resolved tensions with Britain after the Revolutionary War, preventing another war but angering pro-French Americans and revealing deep political divisions in the new republic.",
     json.dumps(["The Jay Treaty was a military alliance between America and France against Britain.",
                  "The Jay Treaty had no significant effect on American foreign policy or domestic politics.",
                  "The Jay Treaty was rejected by both Britain and the United States and never took effect."]),
     "The Jay Treaty (1794), negotiated by Chief Justice John Jay, resolved several outstanding issues between the United States and Britain after the Revolutionary War, including British withdrawal from forts in the Northwest Territory and compensation for seized American ships. While it prevented war with Britain, it was deeply controversial. Pro-French Americans (including Jefferson and Madison) denounced it as too favorable to Britain. The debate over the Jay Treaty helped crystallize the first political party system: Federalists (who supported the treaty) and Democratic-Republicans (who opposed it). Despite the controversy, Washington signed it, arguing it was 'the best we could obtain.'"),
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
