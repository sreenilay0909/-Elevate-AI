"""Playwright-based scrapers for JavaScript-heavy platforms"""
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from typing import Dict, Any
import re
import asyncio

class PlaywrightGFGScraper:
    """GeeksforGeeks scraper using Playwright"""
    
    @staticmethod
    async def fetch_user_data(username: str) -> Dict[str, Any]:
        """
        Fetch GeeksforGeeks data using Playwright (Async)
        
        Args:
            username: GFG username
            
        Returns:
            dict with coding_score, problems_solved, institute_rank, 
            articles_published, longest_streak, potds_solved
        """
        url = f"https://www.geeksforgeeks.org/profile/{username}/?tab=activity"
        
        async with async_playwright() as p:
            try:
                # Launch browser
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Set viewport and user agent
                await page.set_viewport_size({"width": 1920, "height": 1080})
                
                # Navigate to page
                await page.goto(url, wait_until='networkidle', timeout=30000)
                
                # Wait for content to load
                await asyncio.sleep(3)
                
                # Get page content
                content = await page.content()
                
                # Extract data using regex
                def extract_stat(pattern, default=0):
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        value = match.group(1).replace(',', '')
                        return int(value)
                    return default
                
                data = {
                    'coding_score': extract_stat(r'Coding Score[^\d]*(\d+)'),
                    'problems_solved': extract_stat(r'Problems Solved[^\d]*(\d+)'),
                    'institute_rank': extract_stat(r'Institute Rank[^\d]*(\d+)'),
                    'articles_published': extract_stat(r'Articles Published[^\d]*(\d+)'),
                    'longest_streak': extract_stat(r'Longest Streak[^\d]*(\d+)'),
                    'potds_solved': extract_stat(r'POTDs Solved[^\d]*(\d+)'),
                }
                
                await browser.close()
                return data
                
            except PlaywrightTimeout:
                raise ValueError(f"Timeout loading GFG profile for {username}")
            except Exception as e:
                raise ValueError(f"Failed to fetch GFG data: {str(e)}")


class PlaywrightCodeChefScraper:
    """CodeChef scraper using Playwright"""
    
    @staticmethod
    async def fetch_user_data(username: str) -> Dict[str, Any]:
        """
        Fetch CodeChef data using Playwright (Async)
        
        Args:
            username: CodeChef username
            
        Returns:
            dict with current_rating, stars, problems_solved, 
            contests_participated, global_rank, country_rank
        """
        url = f"https://www.codechef.com/users/{username}"
        
        async with async_playwright() as p:
            try:
                # Launch browser
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Set viewport and user agent
                await page.set_viewport_size({"width": 1920, "height": 1080})
                
                # Navigate to page
                await page.goto(url, wait_until='networkidle', timeout=30000)
                
                # Wait for content to load
                await asyncio.sleep(2)
                
                # Get page content
                content = await page.content()
                
                # Extract rating
                def extract_number(text):
                    if not text:
                        return 0
                    match = re.search(r'(\d+)', text.replace(',', ''))
                    return int(match.group(1)) if match else 0
                
                # Extract rating
                rating_match = re.search(r'rating-number[^>]*>(\d+)', content)
                rating = int(rating_match.group(1)) if rating_match else 0
                
                # Calculate stars
                if rating >= 2500:
                    stars = 7
                elif rating >= 2200:
                    stars = 6
                elif rating >= 1800:
                    stars = 5
                elif rating >= 1600:
                    stars = 4
                elif rating >= 1400:
                    stars = 3
                elif rating >= 1200:
                    stars = 2
                else:
                    stars = 1 if rating > 0 else 0
                
                # Extract other stats
                problems_match = re.search(r'Problems Solved[^\d]*(\d+)', content, re.IGNORECASE)
                problems_solved = int(problems_match.group(1)) if problems_match else 0
                
                contests_match = re.search(r'Contests[^\d]*(\d+)', content, re.IGNORECASE)
                contests = int(contests_match.group(1)) if contests_match else 0
                
                global_rank_match = re.search(r'Global Rank[^\d]*(\d+)', content, re.IGNORECASE)
                global_rank = int(global_rank_match.group(1)) if global_rank_match else 0
                
                country_rank_match = re.search(r'Country Rank[^\d]*(\d+)', content, re.IGNORECASE)
                country_rank = int(country_rank_match.group(1)) if country_rank_match else 0
                
                data = {
                    'current_rating': rating,
                    'stars': stars,
                    'problems_solved': problems_solved,
                    'contests_participated': contests,
                    'global_rank': global_rank,
                    'country_rank': country_rank,
                }
                
                await browser.close()
                return data
                
            except PlaywrightTimeout:
                raise ValueError(f"Timeout loading CodeChef profile for {username}")
            except Exception as e:
                raise ValueError(f"Failed to fetch CodeChef data: {str(e)}")
