class FeedManager {
    constructor() {
        this.page = 1;
        this.loading = false;
        this.hasMore = true;
        this.feedContainer = document.querySelector('.feed-container');
        this.setupInfiniteScroll();
        this.setupHashtagDetection();
    }

    setupInfiniteScroll() {
        window.addEventListener('scroll', () => {
            if (this.shouldLoadMore()) {
                this.loadMorePosts();
            }
        });
    }

    shouldLoadMore() {
        if (this.loading || !this.hasMore) return false;
        
        const lastPost = this.feedContainer.lastElementChild;
        if (!lastPost) return false;
        
        const lastPostOffset = lastPost.offsetTop + lastPost.clientHeight;
        const pageOffset = window.pageYOffset + window.innerHeight;
        
        return pageOffset > lastPostOffset - 20;
    }

    async loadMorePosts() {
        this.loading = true;
        this.showLoadingSpinner();

        try {
            const response = await fetch(`/api/posts/?page=${this.page}`);
            const data = await response.json();
            
            if (data.posts.length === 0) {
                this.hasMore = false;
                return;
            }

            this.renderPosts(data.posts);
            this.page += 1;
        } catch (error) {
            console.error('Erreur de chargement:', error);
        } finally {
            this.loading = false;
            this.hideLoadingSpinner();
        }
    }

    setupHashtagDetection() {
        const captionInputs = document.querySelectorAll('.post-caption-input');
        captionInputs.forEach(input => {
            input.addEventListener('input', this.detectHashtags.bind(this));
        });
    }

    detectHashtags(event) {
        const text = event.target.value;
        const hashtags = text.match(/#[a-zA-Z0-9_]+/g) || [];
        
        if (hashtags.length > 0) {
            this.showHashtagSuggestions(hashtags);
        }
    }

    showHashtagSuggestions(hashtags) {
        // Implémentation des suggestions de hashtags
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    const feedManager = new FeedManager();
}); 