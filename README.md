# Landing Page Lead Funnel Validation Tool

## Starting Frontend
```bash
cd frontend
npm run dev
```
## Starting Backend
```bash
cd backend
python server.py
```
## Testing
I created my own sample landing page that has multiple different booking sites: https://sample-booking-site.vercel.app/

## Overview
The general idea to my solution is that we find links to known booking sites, and then proceed to test the booking flow of each link. If there are multiple booking links to multiple sites, we will will test each one of them. 

This approahc comes with upsides:
- It finding the links easier:
  - instead of having to crawl the entire page and see which buttons directed to booking sites, we can just directed find them via built in Selenium functions
However, this design decision comes with a few drawbacks:
- If the landing page uses a booking site that is not supported, my solution won't be able to find and test it

I chose this approach for a few reasons:
- Simplicity: The solution is very straight forward and introduces very few complexities
- Each booking site is unique, so we already have to manually add support for each one.
