[![Build Status](https://travis-ci.org/reticulatingspline/Bible.svg?branch=master)](https://travis-ci.org/reticulatingspline/Bible)

# Limnoria plugin for displaying Bible passages

## Introduction

Plugin for a friend to display Bible passages. 
 
Can display akjv|asv|douayrheims|kjv|web|ylt versions.

## Install

You will need a working Limnoria bot on Python 2.7 for this to work.

Go into your Limnoria plugin dir, usually ~/supybot/plugins and run:

```
git clone https://github.com/reticulatingspline/Bible
```

To install additional requirements, run:

```
pip install -r requirements.txt 
```

or if you don't have or don't want to use root, 

```
pip install -r requirements.txt --user
```


Next, load the plugin:

```
/msg bot load Bible
```

## Example Usage

```
<spline> @bible --version web Job 3:15
<myybot> [WEB] Job 3:15 :: or with princes who had gold, who filled their houses with silver:
<spline> @bible --version kjv Job 3:14
<myybot> [KJV] Job 3:14 :: With kings and counsellers of the earth, which built desolate places for themselves;
```

## About

All of my plugins are free and open source. When I first started out, one of the main reasons I was
able to learn was due to other code out there. If you find a bug or would like an improvement, feel
free to give me a message on IRC or fork and submit a pull request. Many hours do go into each plugin,
so, if you're feeling generous, I do accept donations via Amazon or browse my [wish list](http://amzn.com/w/380JKXY7P5IKE).

I'm always looking for work, so if you are in need of a custom feature, plugin or something bigger, contact me via GitHub or IRC.