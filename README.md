## 2021-08-15: CHECKING NUMBER OF DOWNLOADED CITATIONS

- After running the parsing scripts to separate out citations into single verses, the total number from 1930-2020 is 103214
- Checking on the website, based on the totals shown there, it appears there are a total of 103416
- This leaves 202 citations unaccounted for in the downloaded data, which is likely due to the skipped JST and Headnote sections
- Conclusion: looks like everything got downloaded somehow. Lucky.


## 2021-08-15: DOWNLOADING INDIVIDUAL VERSES

### 1st Nephi Glitch

output looked like this:

```
Rev. ; 22 ; Rev. 22:18 ; https://scriptures.byu.edu/#::fNYNY7267e4110a61618 ; 1981-A:64, Howard W. Hunter ; No Man Shall Add to or Take Away
Rev. ; 22 ; Rev. 22:19 ; https://scriptures.byu.edu/#::fNYNY7267e4110a61619 ; 1981-A:64, Howard W. Hunter ; No Man Shall Add to or Take Away
Rev. ; 22 ; Rev. 22:20 ; https://scriptures.byu.edu/#::fNYNY7267e4110a61620 ; 2009-A:48, Russell M. Nelson ; Lessons from the Lord’s Prayers
Rev. ; 22 ; Rev. 22:21 ; https://scriptures.byu.edu/#::fNYNY7267e4110a61621 ; 2009-A:48, Russell M. Nelson ; Lessons from the Lord’s Prayers
1 Nephi ; https://scriptures.byu.edu/#::fNYNY7267e4110cd ; 2009-A:48, Russell M. Nelson ; Lessons from the Lord’s Prayers
2 Nephi ; 1 ; 2 Ne. 1:5 ; https://scriptures.byu.edu/#::fNYNY7267e4110ce015 ; 1988-O:87, Ezra Taft Benson ; I Testify
2 Nephi ; 1 ; 2 Ne. 1:6 ; https://scriptures.byu.edu/#::fNYNY7267e4110ce016 ; 1975-O:36, Marion G. Romney ; America’s Destiny
2 Nephi ; 1 ; 2 Ne. 1:6 ; https://scriptures.byu.edu/#::fNYNY7267e4110ce016 ; 1975-O:36, Marion G. Romney ; America’s Destiny
2 Nephi ; 1 ; 2 Ne. 1:6 ; https://scriptures.byu.edu/#::fNYNY7267e4110ce016 ; 1975-O:35, Marion G. Romney ; America’s Destiny
```

Somehow the talk from revelations got stuck on the 1 Nephi line and ended up getting 1 nephi skipped altogether
Not sure how that could have happened but something to look for in other cases

Same glitch with Jacob, Jarom, W of M,, 

```
2 Nephi ; 33 ; 2 Ne. 33:15 ; https://scriptures.byu.edu/#::fNYNY7267e4110ce2115 ; 2017-O:63, Russell M. Nelson ; The Book of Mormon: What Would Your Life Be Like without It?
2 Nephi ; 33 ; 2 Ne. 33:15 ; https://scriptures.byu.edu/#::fNYNY7267e4110ce2115 ; 2015-O:130, David A. Bednar ; “Chosen to Bear Testimony of My Name”
Jacob ; https://scriptures.byu.edu/#::fNYNY7267e4110cf ; 2017-O:63, Russell M. Nelson ; The Book of Mormon: What Would Your Life Be Like without It?
Jacob ; https://scriptures.byu.edu/#::fNYNY7267e4110cf ; 2015-O:130, David A. Bednar ; “Chosen to Bear Testimony of My Name”
Enos ; Enos 1:1 ; https://scriptures.byu.edu/#::fNYNY7267e4110d0011 ; 2020-A:40, Gérald Caussé ; A Living Witness of the Living Christ
Enos ; Enos 1:1 ; https://scriptures.byu.edu/#::fNYNY7267e4110d0011 ; 2020-A:26, Douglas D. Holmes ; Deep in Our Heart
Enos ; Enos 1:1 ; https://scriptures.byu.edu/#::fNYNY7267e4110d0011 ; 2019-O:52, Jorge M. Alvarado ; After the Trial of Our Faith
Enos ; Enos 1:1 ; https://scriptures.byu.edu/#::fNYNY7267e4110d0011 ; 2019-A:8, Ulisses Soares ; How Can I Understand?
```

## 2021-08-14: LOOKING AT PARSING TEXT

EXAMPLE STRING:
; 3 Nephi ; 9 ; 3 Ne. 9:15-16,18,20-22 ; https://scriptures.byu.edu/#::fNYNY7267e4130d70915b6B8C0c2 ; 1999-O:72, Russell M. Nelson ; A Testimony of the Book of Mormon





QUESTIONS ABOUT GROUPING:
- Note that there are sometimes multiple replicated citations in a single talk. Do we want to count them separately,
or count the number of talks given by a person with a certain citation in it?

PARSING SCRIPTURE CITATIONS:
- It appears that each scripture reference only ever has a single colon in it
- There are only a few cases Where scripture references do not have a ':' in them:  Title, Intro., 3 Wit., 8 Wit.,
- There are thousands of cases with verse ranges

## 2021-08-14: FIGURING OUT THE HTML STRUCTURE

Inspecting the "Book element" on this page: https://scriptures.byu.edu/#::fNYNY7267e413
This is the book of Genesis button's details:
XPATH:      //*[@id="citationindex2"]/div[1]/div[2]/div[1]/ul[1]/li[1]/a/div[1]
FULL XPATH: /html/body/div[1]/div/div[5]/div[1]/div[2]/div[1]/ul[1]/li[1]/a/div[1]
SELECTOR:   #citationindex2 > div.sciwrapper > div.scicontent.nano.has-scrollbar > div.nano-content > ul:nth-child(3) > li:nth-child(1) > a > div.book

Problem is that sometimes these elements seem to fall under citationindex rather than citationindex2 (not sure why)
However, it appears that (at least for the root page) the class 'sciwrapper' is a reliable selector of the right-pane

Recap of element names and attributes at each "level" of citation index:

- LEVEL 1: VOLUMES
<div class="sciwrapper">
    <div class="scicontent nano has-scrollbar">
        <div class="nano-content" tabindex="0">
            <div class="volumetitle">
            <ul class="volumecontents">
                <li class="grid">
                    <a href="javascript:void(0);" onclick="getFilter('101')">
                        <div class="book">Genesis</div>
                        <div class="citationcount">[609]</div>
                        
- LEVEL 2: CHAPTERS
<div class="sciwrapper">
    <div class="scicontent nano has-scrollbar">
        <div class="nano-content" tabindex="0">
            <b class="chaptertitle">
            <ul class="chaptersblock">
                <li>
                    <a href="javascript:void(0);" onclick="getFilter('101', '1')">
                        <div class="chap">1</div>
                        <div class="citationcount">[87]</div>

- LEVEL 3: VERSES
<div class="sciwrapper">
    <div class="scicontent nano has-scrollbar">
        <div class="nano-content" tabindex="0">
            <ul class="referencesblock">
                <li>
                    <a href="javascript:void(0);" onclick="getFilter('101', '1', '1', '')">
                        <div class="reference">Gen. 1:1</div>
                        <div class="citationcount">[3]</div>
                        
- LEVEL 4: TALKS
<div class="sciwrapper">
    <div class="scicontent nano has-scrollbar">
        <div class="nano-content" tabindex="0">
            <div class="volumetitle">
            <ul class="referencesblock">
                <li>
                    <a href="javascript:void(0);" class="refcounter" onclick="getTalk('8226', '132593');">
                        <div class="reference referencewatch referencelisten">2017-A:19, Henry B. Eyring</div>
                        <div class="talktitle talktitlewatch talktitlelisten">Gethering the Family of God</div>







- Talks are numbered with hexadecimal from 1 (April 1942) to 210b (April 2020)
- Format is `https://scriptures.byu.edu/#:t<talknumber>`

## Citations:
- `<span class="citation" id="130466"><a href="javascript:void(0)" onclick="sx(this, 130466)">&nbsp;</a><a href="javascript:void(0)" onclick="gs(130466)">1&nbsp;Corinthians 11:11</a></span>`


## Talk Details:
- found in div, id='talklabel'
- string content: "<year>-<month-initial>:<talknumber>, <speaker_name>, <title>"
`<div id="talklabel" class="visiblelabel"><a href="javascript:void(0);" onclick="getConf('2015', 'A');">2015–A</a>:14, Bonnie L. Oscarson, Defenders of the Family Proclamation</div>`


```
import requests
r = requests.get(url)
with open('text.txt', 'w', encoding='utf-8') as f:
    f.write(r.text)
```

d2e664b: having issues after 0x720 because 0x721 doesn't exist.
- Weirdly, the talk 0x720 is in between 0x631 and 0x632 (1967 October)

https://scriptures.byu.edu/#:t630:g889
https://scriptures.byu.edu/#:t631:g889
https://scriptures.byu.edu/#:t720:g889 (??????)
https://scriptures.byu.edu/#:t632:g889
https://scriptures.byu.edu/#:t633:g889
etc...


- 0x719: https://scriptures.byu.edu/#:t719 is (1970 October)


OCT 1970: 6f7-71f (i.e 1783-1823)
APR 1971: 7d0-7fb (i.e. 2000-2043)

Also, 0x721 



8361 is the last talk that has a id='primary' marker for the main body
(i.e. things are different starting in 2019-A)


## Footnotes
- First instance: talk 3672


## By Scripture:
citation index: https://scriptures.byu.edu/#::fNYNY7267e401 (1919411201)


## By Scripture (full citation):
- citation index: https://scriptures.byu.edu/#::c
- Genesis:        https://scriptures.byu.edu/#::c065
- Genesis 1:      https://scriptures.byu.edu/#::c06501
- Genesis 1:1:    https://scriptures.byu.edu/#::c065011
- Genesis 1:1-2:  https://scriptures.byu.edu/#::c065011c
- Genesis 1:1-3:  https://scriptures.byu.edu/#::c065011d
- Genesis 2:      https://scriptures.byu.edu/#::c06502
- Genesis 2:1 JST https://scriptures.byu.edu/#::c465021
- Genesis 3:1     https://scriptures.byu.edu/#::c065031

OT:
Genesis 065 (101)
Exodus  066 (102)
...
Malachi 08b (139)

NT:
Matthew 08c (140)
...
Revelation 0a6 (166)

BOM
...

AofF: 196 (406)



pattern: "https://scriptures.byu.edu/#::c bbb cc"
listed individually: "https://scriptures.byu.edu/#::fNYNY7267e401 bbb cc "


## Plan for new approach:
- Start: 'https://scriptures.byu.edu/#::fNYNY7267e401'


## Good Refs
- https://scripturetools.net/statistics
