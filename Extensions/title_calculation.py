def title(totalQuestions, totalQuestionsAnswered):
    twentyPercent = 0.2
    fortyPercent = 0.4
    sixtyPercent = 0.6
    eightyPercent = 0.8
        
    calculatedTitle = ""
    total_progression = totalQuestionsAnswered / totalQuestions

    if total_progression < twentyPercent:
        calculatedTitle = "Phishing Awareness Level 1: The Unaware User"
    elif total_progression > twentyPercent and total_progression < fortyPercent:
        calculatedTitle = "Phishing Awareness Level 2: The Cautious Beginner"
    elif total_progression > fortyPercent and total_progression < sixtyPercent:
        calculatedTitle = "Phishing Awareness Level 3: The Informed User"
    elif total_progression > sixtyPercent and total_progression < eightyPercent:
        calculatedTitle = "Phishing Awareness Level 4: The Savvy Defender"
    else:
        calculatedTitle = "Phishing Awareness Level 5: The Expert Analyst"

    return calculatedTitle
