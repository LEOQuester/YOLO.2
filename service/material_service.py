import requests
from genres import GENRE_DATA
class Material():
    def __intit__(self):
        pass

    def media_from_keywords(self, keywords, media_type):
        url = "https://api.themoviedb.org/3/discover/" + media_type
        api_key = "7e16229611389f1788334e9c9ee5d934"
        keyword_ids = self._get_keyword_ids(api_key, keywords)
        keywords_str = '|'.join(map(str, keyword_ids))
        params = {
            'api_key': api_key,
            'with_keywords': keywords_str
        }

        #search_from_titles(keywords)

        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                movies_data = response.json()

                if 'results' in movies_data:
                    for movie in movies_data['results']:
                        # Check if 'genre_ids' is present in the movie object
                        if 'genre_ids' in movie:
                            # Replace genre IDs with genre names
                            genre_names = []
                            for genre_id in movie['genre_ids']:
                                # Use next to get the first match or None if not found
                                genre = next((g for g in GENRE_DATA if g['id'] == genre_id), None)
                                if genre:
                                    genre_names.append(genre['name'])
                            movie['genres'] = genre_names
                            # Remove 'genre_ids' as it's no longer needed
                            del movie['genre_ids']

                        # Check if 'poster_path' is present in the movie object
                        if 'poster_path' in movie:
                            # Construct the complete URL for the poster
                            movie['poster_path'] = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"

                    # Return the updated list of movie objects
                    return movies_data['results']
                else:
                    print("Error: 'results' key not found in the response.")
                    return None
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def _get_keyword_ids(self, api_key, keyword):
        url = f"https://api.themoviedb.org/3/search/keyword"
        keyword_ids = []

        for word in keyword:
            params = {
                'api_key': api_key,
                'query': word
            }

            try:
                response = requests.get(url, params=params)

                if response.status_code == 200:
                    keyword_data = response.json()
                    if 'results' in keyword_data:
                        # Get the top 5 keyword IDs for each word
                        word_ids = [kw['id'] for kw in keyword_data['results'][:5]]
                        keyword_ids.extend(word_ids)
                    else:
                        print(f"Error: 'results' key not found in the response for {word}.")
                else:
                    print(f"Error: {response.status_code} - {response.text} for {word}")

                time.sleep(1)  # Introduce a 1-second delay between API calls

            except Exception as e:
                print(f"An error occurred for {word}: {e}")

        return keyword_ids
        
    def get_songs(self, keywords, media_type):
        if media_type == 'song':
            keywords.append('official music videos')
        if media_type == 'video':
            keywords.append('videos only')    
        q = ' '.join(keywords)

        api_key = "AIzaSyD1CFHMw7mPYugkVMCoeRd69HPDOlchJUo"
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'q': q,
            'part': 'snippet',
            'maxResults': '20',
            'type': 'video',
            'order': 'rating',
            'key': api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for bad requests

            # Extract relevant information from the API response
            videos = response.json().get('items', [])

            # Customize the return object for each video
            formatted_videos = []
            for video in videos:
                formatted_video = {
                    'thumbnail': video['snippet']['thumbnails']['medium']['url'],
                    'title': video['snippet']['title'],
                    'video_url': f"https://www.youtube.com/watch?v={video['id']['videoId']}",
                    'publishDate': video['snippet']['publishTime']
                }
                formatted_videos.append(formatted_video)

            return formatted_videos

        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")
            return None

    def get_books(self, keywords):
        print(keywords)
        url = "https://www.googleapis.com/books/v1/volumes"
        q = ' '.join(keywords)
        params = {'q': q}

        try:
            response = requests.get(url, params=params)
            print(response.json())
            response.raise_for_status()  # Raise an exception for bad requests
            data = response.json()

            # Customized return object list
            books_list = []
            for item in data.get("items", []):
                volume_info = item.get("volumeInfo", {})
                image_links = volume_info.get("imageLinks", {})
                
                thumbnail = image_links.get("thumbnail", "https://cdn.bookauthority.org/dist/images/book-cover-not-available.6b5a104fa66be4eec4fd16aebd34fe04.png")
                
                book_info = {
                    "thumbnail": thumbnail if thumbnail else "https://cdn.bookauthority.org/dist/images/book-cover-not-available.6b5a104fa66be4eec4fd16aebd34fe04.png",
                    "title": volume_info.get("title", "Data not available"),
                    "textSnippet": item.get("searchInfo", {}).get("textSnippet", "Data not available"),
                    "description": volume_info.get("description", "Data not available"),
                    "contentUrl": volume_info.get("previewLink", "Data not available"),
                    "publishDate": volume_info.get("publishedDate", "Data not available"),
                    "publisher": volume_info.get("publisher", "Data not available"),
                    "language": volume_info.get("language", "Data not available"),
                    "maturity": volume_info.get("maturityRating", "Data not available"),
                }
                books_list.append(book_info)

            return books_list

        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")
            return None

    def get_anime(self, keywords, media_type):
        url = "https://api.jikan.moe/v4/anime"  
        q = ' '.join(keywords)
        params = {
            'q': q,
            'type': media_type
        }

        try:
            # Hit the API call and get the response object
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            response_json = response.json()

            # Customized return object list
            anime_list = []
            for item in response_json.get("data", []):
                images = item.get("images", {})
                thumbnail = images.get("jpg", {}).get("image_url", "Data not available")

                titles = item.get("titles", [])
                title = next((t.get("title", "Data not available") for t in titles if t.get("type") == "Default"), "Data not available")
                japanese_title = next((t.get("title", "Data not available") for t in titles if t.get("type") == "Japanese"), "Data not available")

                synopsis = item.get("synopsis", "Data not available")
                more_info_url = item.get("url", "Data not available")

                genres = [genre.get("name", "Data not available") for genre in item.get("genres", [])]
                themes = [theme.get("name", "Data not available") for theme in item.get("themes", [])]

                release_year = item.get("aired", {}).get("prop", {}).get("from", {}).get("year", "Data not available")
                producers = [producer.get("name", "Data not available") for producer in item.get("producers", [])]
                episodes_count = item.get("episodes", "Data not available")
                rating = item.get("rating", "Data not available")

                anime_info = {
                    "thumbnail": thumbnail,
                    "title": title,
                    "japanese_title": japanese_title,
                    "synopsis": synopsis,
                    "moreinfo_url": more_info_url,
                    "genres": genres,
                    "themes": themes,
                    "release_year": release_year,
                    "producers": producers,
                    "episodes_count": episodes_count,
                    "rating": rating,
                }
                anime_list.append(anime_info)

            return anime_list

        except requests.exceptions.RequestException as e:
            print(f"Error in making the request: {e}")
            return []

        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

    def media_from_title(self, title, media_type):
        """
        Search for media (movies or TV shows) based on the title.

        Parameters:
        - title: String containing the title to search for.
        - media_type: String specifying the type of media (e.g., "movie" or "tv").

        Returns:
        - List of media objects with updated poster URLs and genre names.
        """
        url = f"https://api.themoviedb.org/3/search/{media_type}"
        api_key = "7e16229611389f1788334e9c9ee5d934"
        params = {'api_key': api_key, 'query': title}

        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                media_data = response.json()

                if 'results' in media_data:
                    for item in media_data['results']:
                        # Check if 'genre_ids' is present in the media object
                        if 'genre_ids' in item:
                            # Replace genre IDs with genre names
                            genre_names = []
                            for genre_id in item['genre_ids']:
                                # Use next to get the first match or None if not found
                                genre = next((g for g in GENRE_DATA if g['id'] == genre_id), None)
                                if genre:
                                    genre_names.append(genre['name'])
                            item['genres'] = genre_names
                            # Remove 'genre_ids' as it's no longer needed
                            del item['genre_ids']

                        # Check if 'poster_path' is present in the media object
                        if 'poster_path' in item:
                            # Construct the complete URL for the poster
                            item['poster_path'] = f"https://image.tmdb.org/t/p/w500{item['poster_path']}"

                    # Return the updated list of media objects
                    return media_data['results']
                else:
                    print("Error: 'results' key not found in the response.")
                    return None
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        