

GSM8K_PROMPT = """Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?\nA: There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6. The answer is 6.\n\n\
Q: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?\nA: There are originally 3 cars. 2 more cars arrive. 3 + 2 = 5. The answer is 5.\n\n\
Q: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?\nA: Originally, Leah had 32 chocolates. Her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they had 74 - 35 = 39. The answer is 39.\n\n\
Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?\nA: Jason started with 20 lollipops. Then he had 12 after giving some to Denny. So he gave Denny 20 - 12 = 8. The answer is 8.\n\n\
Q: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?\nA: Shawn started with 5 toys. If he got 2 toys each from his mom and dad, then that is 4 more toys. 5 + 4 = 9. The answer is 9.\n\n\
Q: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?\nA: There were originally 9 computers. For each of 4 days, 5 more computers were added. So 5 * 4 = 20 computers were added. 9 + 20 is 29. The answer is 29.\n\n\
Q: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?\nA: Michael started with 58 golf balls. After losing 23 on tuesday, he had 58 - 23 = 35. After losing 2 more, he had 35 - 2 = 33 golf balls. The answer is 33.\n\n\
Q: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?\nA: Skeleton:\n1. Olivia starts with $23.\n2. Buys 5 bagels.\n3. Each bagel costs $3.\n4. Subtract total cost.\n5. Calculate remaining money.\nReasoning:\n1. Olivia starts with $23.\n2. Buys 5 bagels.\n3. Each bagel costs $3.\n4. Subtract total cost. Multiply the cost per bagel ($3) by the number of bagels (5) to find the total cost and subtract it from Olivia's initial amount.\n5. Calculate remaining money. Subtracting the total cost of the bagels from Olivia's initial $23, she has $8 left. The answer is 8.\n\n\
Q: """

MMLU_PROMPT = """The following are multiple choice questions (with answers) about global\
  \ facts.\n\nQ: As of 2017, how many of the world’s 1-year-old children today have\
  \ been vaccinated against some disease? *\n(A) 80% (B) 60% (C) 40% (D) 20%\nA: Let's\
  \ think step by step. We refer to Wikipedia articles on global facts for help. According\
  \ to data published by the World Health Organization, the nummber of 1-year-old\
  \ children vaccinated in 2017 exceeds 80%. The answer is (A).\n\nQ: As of 2019,\
  \ about what percentage of Americans agree that the state is run for the benefit\
  \ of all the people?\n(A) 31% (B) 46% (C) 61% (D) 76%\nA: Let's think step by step.\
  \ We refer to Wikipedia articles on global facts for help. In 2019, about 46% percentage\
  \ of Americans agree that the state is run for the benefit of all the people. The\
  \ answer is (B).\n\nQ: As of 2019, about what percentage of Russians say it is very\
  \ important to have free media in our country without government/state censorship?\n\
  (A) 38% (B) 53% (C) 68% (D) 83%\nA: Let's think step by step. We refer to Wikipedia\
  \ articles on global facts for help. As of 2019, about 38% of Russians say it is\
  \ very important to have free media in our country. The answer is (A).\n\nQ: As\
  \ of 2015, since 1990 forests have ____ in Europe and have ____ in Africa and the\
  \ Americas.\n(A) increased, increased (B) increased, decreased (C) decreased, increased\
  \ (D) decreased, decreased\nA: Let's think step by step. We refer to Wikipedia articles\
  \ on global facts for help. As of 2015, since 1990 forests have increased in Europe\
  \ and have decreased in Africa and the Americas. The answer is (B).\n\nQ: Which\
  \ of the following pairs of statements are both true (as of 2019)?\n(A) People tend\
  \ to be optimistic about their own future and the future of their nation or the\
  \ world. (B) People tend to be optimistic about their own future but pessimistic\
  \ about the future of their nation or the world. (C) People tend to be pessimistic\
  \ about their own future but optimistic about the future of their nation or the\
  \ world. (D) People tend to be pessimistic about their own future and the future\
  \ of their nation or the world.\nA: Let's think step by step. We refer to Wikipedia\
  \ articles on global facts for help. As of 2019, most people tend to be optimistic\
  \ about their own future but pessimistic about the future of their nation or the\
  \ world. The answer is (B).\n\nQ: """


BBH_PROMPT = """Q: not ( ( not not True ) ) is\nA: False\n\n \
  Q: True and False and not True and True is\nA: False\n\n \
  Q: not not ( not ( False ) ) is\nA: True\n\nQ: """