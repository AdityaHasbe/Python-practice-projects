# storing questions based on category (science, geography, maths, gk)
question_storage = {
    "easy_science": [
        {"question": "What planet do we live on?", "options": "A) Mars, B) Earth, C) Venus, D) Mercury", "answer": "B"},
        {"question": "Which gas do plants use to make their food?", "options": "A) Oxygen, B) Carbon Dioxide, C) Nitrogen, D) Hydrogen", "answer": "B"},
        {"question": "What is the boiling point of water?", "options": "A) 100°C, B) 0°C, C) 100°F, D) 0°F", "answer": "A"},
        {"question": "Which part of the plant makes food?", "options": "A) Root, B) Stem, C) Flower, D) Leaf", "answer": "D"},
        {"question": "What force pulls objects toward the ground?", "options": "A) Magnetism, B) Friction, C) Gravity, D) Electricity", "answer": "C"}
    ],

    "medium_science": [
        {"question": "Which planet is known as the Red Planet?", "options": "A) Jupiter, B) Mars, C) Saturn, D) Venus", "answer": "B"},
        {"question": "What is H2O commonly known as?", "options": "A) Salt, B) Water, C) Oxygen, D) Hydrogen", "answer": "B"},
        {"question": "What is the main gas in the air we breathe?", "options": "A) Oxygen, B) Carbon dioxide, C) Nitrogen, D) Hydrogen", "answer": "C"},
        {"question": "What part of the eye controls how much light enters?", "options": "A) Retina, B) Cornea, C) Pupil, D) Iris", "answer": "C"},
        {"question": "Which planet has rings around it?", "options": "A) Saturn, B) Mars, C) Mercury, D) Venus", "answer": "A"}
    ],

    "hard_science": [
        {"question": "What is the powerhouse of the cell?", "options": "A) Nucleus, B) Mitochondria, C) Ribosome, D) Chloroplast", "answer": "B"},
        {"question": "What is the speed of light?", "options": "A) 300,000 km/s, B) 150,000 km/s, C) 100,000 km/s, D) 1,000 km/s", "answer": "A"},
        {"question": "Which element has the atomic number 1?", "options": "A) Helium, B) Hydrogen, C) Oxygen, D) Carbon", "answer": "B"},
        {"question": "What is the process by which plants release water vapor?", "options": "A) Photosynthesis, B) Respiration, C) Transpiration, D) Evaporation", "answer": "C"},
        {"question": "What is the chemical formula of table salt?", "options": "A) NaCl, B) KCl, C) NaCO3, D) HCl", "answer": "A"}
    ],

    "easy_geography": [
        {"question": "What is the largest continent?", "options": "A) Africa, B) Asia, C) Europe, D) Antarctica", "answer": "B"},
        {"question": "Which ocean is the largest?", "options": "A) Atlantic, B) Indian, C) Pacific, D) Arctic", "answer": "C"},
        {"question": "What is the capital of France?", "options": "A) Berlin, B) Paris, C) London, D) Madrid", "answer": "B"},
        {"question": "Which country is famous for the Great Wall?", "options": "A) India, B) China, C) Japan, D) Korea", "answer": "B"},
        {"question": "Which river is the longest in the world?", "options": "A) Nile, B) Amazon, C) Yangtze, D) Mississippi", "answer": "A"}
    ],

    "medium_geography": [
        {"question": "Which is the smallest country in the world?", "options": "A) Monaco, B) Vatican City, C) Malta, D) San Marino", "answer": "B"},
        {"question": "Mount Everest is located in which country?", "options": "A) India, B) Nepal, C) China, D) Bhutan", "answer": "B"},
        {"question": "Which ocean is between Africa and Australia?", "options": "A) Pacific, B) Indian, C) Atlantic, D) Arctic", "answer": "B"},
        {"question": "Which country has the most population?", "options": "A) India, B) USA, C) China, D) Russia", "answer": "C"},
        {"question": "Which US state is famous for the Grand Canyon?", "options": "A) Arizona, B) Utah, C) Nevada, D) Colorado", "answer": "A"}
    ],

    "hard_geography": [
        {"question": "What is the deepest ocean trench?", "options": "A) Mariana Trench, B) Tonga Trench, C) Java Trench, D) Philippine Trench", "answer": "A"},
        {"question": "Which country has the longest coastline?", "options": "A) Australia, B) USA, C) Canada, D) Russia", "answer": "C"},
        {"question": "Which desert is located in northern China and southern Mongolia?", "options": "A) Gobi, B) Sahara, C) Kalahari, D) Atacama", "answer": "A"},
        {"question": "Which is the largest freshwater lake by area?", "options": "A) Lake Victoria, B) Lake Superior, C) Lake Baikal, D) Lake Tanganyika", "answer": "B"},
        {"question": "Which mountain range separates Europe and Asia?", "options": "A) Alps, B) Himalayas, C) Ural, D) Andes", "answer": "C"}
    ],

    "easy_maths": [
        {"question": "What is (5 + 3) ?", "options": "A) 7, B) 8, C) 9, D) 10", "answer": "B"},
        {"question": "What is (10 - 4 )?", "options": "A) 5, B) 6, C) 7, D) 8", "answer": "B"},
        {"question": "What is (3 × 4) ?", "options": "A) 12, B) 14, C) 15, D) 16", "answer": "A"},
        {"question": "What is (16 ÷ 4) ?", "options": "A) 2, B) 3, C) 4, D) 5", "answer": "C"},
        {"question": "What is the square of 5?", "options": "A) 10, B) 15, C) 20, D) 25", "answer": "D"}
    ],

    "medium_maths": [
        {"question": "What is 12 × 12?", "options": "A) 124, B) 144, C) 154, D) 164", "answer": "B"},
        {"question": "What is 100 ÷ 5?", "options": "A) 15, B) 20, C) 25, D) 30", "answer": "C"},
        {"question": "What is the square root of 81?", "options": "A) 8, B) 9, C) 10, D) 11", "answer": "B"},
        {"question": "What is 7²?", "options": "A) 47, B) 49, C) 51, D) 57", "answer": "B"},
        {"question": "What is 15% of 200?", "options": "A) 25, B) 30, C) 35, D) 40", "answer": "B"}
    ],

    "hard_maths": [
        {"question": "Solve: 2x + 5 = 15", "options": "A) 3, B) 4, C) 5, D) 6", "answer": "C"},
        {"question": "What is the derivative of x²?", "options": "A) x, B) 2x, C) x², D) 2", "answer": "B"},
        {"question": "What is the integral of 2x dx?", "options": "A) x² + C, B) x², C) 2x² + C, D) 2x²", "answer": "A"},
        {"question": "What is 15 × 14?", "options": "A) 200, B) 210, C) 215, D) 220", "answer": "B"},
        {"question": "What is log10 100?", "options": "A) 1, B) 2, C) 10, D) 100", "answer": "B"}
    ],

    "easy_gk": [
        {"question": "Who is the first President of the USA?", "options": "A) Abraham Lincoln, B) George Washington, C) Thomas Jefferson, D) John Adams", "answer": "B"},
        {"question": "What color do you get by mixing red and white?", "options": "A) Pink, B) Purple, C) Orange, D) Brown", "answer": "A"},
        {"question": "How many continents are there?", "options": "A) 5, B) 6, C) 7, D) 8", "answer": "C"},
        {"question": "Which is the fastest land animal?", "options": "A) Lion, B) Tiger, C) Cheetah, D) Leopard", "answer": "C"},
        {"question": "Which is the largest mammal?", "options": "A) Elephant, B) Blue Whale, C) Hippo, D) Giraffe", "answer": "B"}
    ],

    "medium_gk": [
        {"question": "Which continent is known as the 'Dark Continent'?", "options": "A) Africa, B) Asia, C) Europe, D) South America", "answer": "A"},
        {"question": "Who invented the telephone?", "options": "A) Alexander Graham Bell, B) Thomas Edison, C) Nikola Tesla, D) Guglielmo Marconi", "answer": "A"},
        {"question": "Which planet is known as the 'Morning Star'?", "options": "A) Venus, B) Mars, C) Mercury, D) Jupiter", "answer": "A"},
        {"question": "Which country is called the Land of the Rising Sun?", "options": "A) China, B) Japan, C) Korea, D) Thailand", "answer": "B"},
        {"question": "Who wrote 'Romeo and Juliet'?", "options": "A) Charles Dickens, B) William Shakespeare, C) Jane Austen, D) Mark Twain", "answer": "B"},
        {"question": "Which is the longest river in Asia?", "options": "A) Yangtze, B) Ganges, C) Mekong, D) Yellow River", "answer": "A"}
    ],

    "hard_gk": [
        {"question": "Who discovered penicillin?", "options": "A) Louis Pasteur, B) Alexander Fleming, C) Marie Curie, D) Isaac Newton", "answer": "B"},
        {"question": "Which is the smallest bone in the human body?", "options": "A) Femur, B) Stapes, C) Tibia, D) Radius", "answer": "B"},
        {"question": "Which country hosted the 2016 Summer Olympics?", "options": "A) China, B) Brazil, C) UK, D) Russia", "answer": "B"},
        {"question": "What is the hardest natural substance on Earth?", "options": "A) Diamond, B) Gold, C) Iron, D) Quartz", "answer": "A"},
        {"question": "Which scientist proposed the theory of relativity?", "options": "A) Isaac Newton, B) Albert Einstein, C) Galileo Galilei, D) Niels Bohr", "answer": "B"}
    ],

    "easy_mixed": [{"question": "What planet do we live on?", "options": "A) Mars, B) Earth, C) Venus, D) Mercury", "answer": "B"},
                    {"question": "What is 5 + 3?", "options": "A) 7, B) 8, C) 9, D) 10", "answer": "B"},
                    {"question": "Who is the first President of the USA?", "options": "A) Abraham Lincoln, B) George Washington, C) Thomas Jefferson, D) John Adams", "answer": "B"},
                    {"question": "Which gas do plants use to make their food?", "options": "A) Oxygen, B) Carbon Dioxide, C) Nitrogen, D) Hydrogen", "answer": "B"},
                    {"question": "What is the largest continent?", "options": "A) Africa, B) Asia, C) Europe, D) Antarctica", "answer": "B"}],

    "medium_mixed": [{"question": "Which is the longest river in Asia?", "options": "A) Yangtze, B) Ganges, C) Mekong, D) Yellow River", "answer": "A"},
                    {"question": "Which city is known as the 'City of Canals'?", "options": "A) Amsterdam, B) Venice, C) Bangkok, D) Bruges", "answer": "B"},
                    {"question": "What is 12 × 12?", "options": "A) 124, B) 144, C) 154, D) 164", "answer": "B"},
                    {"question": "What is 100 ÷ 5?", "options": "A) 15, B) 20, C) 25, D) 30", "answer": "C"},
                    {"question": "Which part of the plant makes food?", "options": "A) Root, B) Stem, C) Flower, D) Leaf", "answer": "D"}],
    
    "hard_mixed": [{"question": "Who discovered penicillin?", "options": "A) Louis Pasteur, B) Alexander Fleming, C) Marie Curie, D) Isaac Newton", "answer": "B"},
                   {"question": "Solve: 2x + 5 = 15", "options": "A) 3, B) 4, C) 5, D) 6", "answer": "C"},
                    {"question": "What is the process by which plants release water vapor?", "options": "A) Photosynthesis, B) Respiration, C) Transpiration, D) Evaporation", "answer": "C"},
                    {"question": "What is the chemical formula of table salt?", "options": "A) NaCl, B) KCl, C) NaCO3, D) HCl", "answer": "A"},
                    {"question": "Which vitamin is produced when sunlight hits the skin?", "options": "A) Vitamin A, B) Vitamin B12, C) Vitamin C, D) Vitamin D", "answer": "D"}]
}