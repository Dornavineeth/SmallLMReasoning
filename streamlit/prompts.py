

GSM8K_PROMPT = """Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?\nA: There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6. The answer is 6.\n\n\
Q: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?\nA: Skeleton:\n1. Start with 3 cars.\n2. Add 2 more cars.\n3. Total cars?\nReasoning:\n1. Start with 3 cars.\n2. Add 2 more cars.\n3. Total cars? Combine the initial 3 cars with the additional 2 cars, resulting in a total of 5 cars in the parking lot. The answer is 5.\n\n\
Q: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?\nA: Originally, Leah had 32 chocolates. Her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they had 74 - 35 = 39. The answer is 39.\n\n\
Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?\nA: Jason started with 20 lollipops. Then he had 12 after giving some to Denny. So he gave Denny 20 - 12 = 6. The answer is 6.\nThis is an incorrect answer, an error occurred in the subtraction step. It incorrectly states that Jason gave Denny 20 - 12 = 6 lollipops, which is not accurate. The correct subtraction should be 20 - 12 = 8.\n\n\
Q: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?\nA: Shawn started with 5 toys. If he got 2 toys each from his mom and dad, then that is 4 more toys. 5 + 4 = 9. The answer is 9.\n\n\
Q: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?\nA: A: There were originally 9 computers. For each of 4 days, 5 more computers were added. So 5 * 4 = 20 computers were added. Therefore, the incorrect calculation would be 9 - 20, which is -11. This is an incorrect answer, as it introduces a subtraction instead of addition at the reasoning stage. The correct reasoning should be 9 + 20 = 29.\n\n\
Q: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?\nA: Olivia had 23 dollars. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. So she has 23 - 15 dollars left. 23 - 15 is 8. The answer is 8.\n\n\
Q: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?\nA: Skeleton:\n1. Michael starts with 58 golf balls.\n2. On Tuesday, he loses 23.\n3. On Wednesday, he loses 2 more.\n4. Subtract losses from the total.\n5. Final count on Wednesday?.\nReasoning:\n1. Michael starts with 58 golf balls.\n2. On Tuesday, he loses 23.\n3. On Wednesday, he loses 2 more.\n4. Subtract losses from the total. Subtracting the losses of 23 on Tuesday and 2 on Wednesday from the initial count, Michael is left with 33 golf balls.\n5. Final count on Wednesday? Michael has 33 golf balls at the end of Wednesday. The answer is 33.\n\n\
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