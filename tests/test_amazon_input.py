from pathlib import Path

from src.sentiment_analysis.amazon_input import AmazonJsonFile
from src.sentiment_analysis.analyze import Analyzer


def test_read_json_file():
    amazon = AmazonJsonFile(Path('assets/reviewsAmazon.json'))
    long_review = "I will start by saying that it really could be an amazing product with just a few simple changes. I bought this product and was really excited to use it. Mounts on any overlay about 2 inches thick or less. Very light and sturdy for what it does. Awesome variable speed feature that can be really helpful when cutting materials with different hardness. The reason I give this product 2 stars (and returned it) is because of the blades it uses and comes with. It comes with pin ended blades and can only use pin ended blades. What that means is that while using the saw, I went through 10 out of the 10 blades it came with because of the pins popping out of the blade end. I tried fitting the pins back into the blades and reusing them but they just popped out again after some use. The fun part was trying to get more blades. I couldn't find any retailer in my area that carried them and ordering them online was not convenient because the shipping cost just about as much as the blades did. So the Saw was a great price at $99, Blades are absolutely horrible to use and not cost effective to buy. I was told that the blades used in standard scroll saws would not work on this saw because the 3\" blades would be too small and the 5\" blades extend farther than the pin holder prongs. I did return the saw because of these factors. There are plenty of other choices for scroll saws out there but based on what I have researched, I bought the DeWalt 788 scroll saw with it's stand. I am Very Very happy with my 788 but as for this little guy, it is simply not worth the headache. If I was able to use plain ended standard sized blades with it, I would of most likely given it a full 5 stars,and kept it, as it was definitely as space saver compared to the DeWalt 788. Hope this helps."
    assert amazon.data[0] == long_review


def test_analyze_result():
    amazon = AmazonJsonFile(Path('assets/reviewsAmazon.json'))
    analyzer = Analyzer(amazon)
    analyzer.get_sentiment_values()
    match_count = 0
    neutral_error = 0
    for i in range(len(amazon.stars)):
        [pos, neg, _] = analyzer.sentiment_values[i]
        positive = pos > neg
        if amazon.stars[i] > 3 and positive:
            match_count += 1
        elif amazon.stars[i] < 3 and not positive:
            match_count += 1
        elif amazon.stars[i] == 3 and pos == neg:
            match_count += 1
        elif pos == neg:
            neutral_error += 1
    print(
        f"match count: {match_count}/{len(amazon.stars)}, neutral error: {neutral_error}"
    )
    assert match_count + neutral_error >= len(amazon.stars) / 2
