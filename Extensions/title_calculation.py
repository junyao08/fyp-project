def title(totalQuestions, totalQuestionsAnswered):
    twentyPercent = 0.2 * 100
    fortyPercent = 0.4 * 100
    sixtyPercent = 0.6 * 100
    eightyPercent = 0.8 * 100
        
    calculatedTitle = ""
    tracker = totalQuestionsAnswered / totalQuestions

    if tracker < twentyPercent:
        calculatedTitle = "Phishing Awareness Level 1: The Unaware User"
    elif tracker > twentyPercent and tracker < fortyPercent:
        calculatedTitle = "Phishing Awareness Level 2: The Cautious Beginner"
    elif tracker > fortyPercent and tracker < sixtyPercent:
        calculatedTitle = "Phishing Awareness Level 3: The Informed User"
    elif tracker > sixtyPercent and tracker < eightyPercent:
        calculatedTitle = "Phishing Awareness Level 4: The Savvy Defender"
    else:
        calculatedTitle = "Phishing Awareness Level 5: The Expert Analyst"

    return calculatedTitle
