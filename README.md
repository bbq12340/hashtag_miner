CONCEPT

*INSERT A HASHTAG AND RECEIVE AN CSV FILE OF HASHTAG RECOMMENDATION

Todo
1. insert handle function ( hastag , requested number of hastags )
2. search the inserted hastag in instagram
    - amount of posts
    - related hastags ( always 10 )
    1 -> 11 -> 111
3. search the related hastags ( that has the high post amounts )
    - loop the process of 2nd step
4. run the code at *time
    - set intervals for the highest increase
5. get the hastag for the most highest increase
6. result: write csvfile 
    - num. of rows: requested amount
    - avg of increase in the set intervals

# README
The basic math:
1. search parent tag
2. get the list of related tags until it has 100 elem
3. search every elem in the list -> get counts
4. loop step3 for defined sets(sets of loops), intervals(intervals between sets) -> "hashtag.csv"
5. read "hashtag.csv" -> analyze into "analysis.csv"
    index: hastags
    columns:
    - latest counts
    - hottest peak time
    - 2nd hottest peak time
    - average of icrease rate/*intervals(minutes)

# UPDATE 2020/08/06
# Instagram disables related hashtags feature after bug that appeared to favor Trump (2020.08.05)
    


