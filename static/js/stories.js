class StoriesManager {
    constructor() {
        this.currentStory = null;
        this.stories = [];
        this.setupStoryModal();
        this.loadStories();
    }

    setupStoryModal() {
        this.modal = new bootstrap.Modal(document.getElementById('storyModal'));
        this.setupNavigationControls();
    }

    async loadStories() {
        try {
            const response = await fetch('/api/stories/');
            this.stories = await response.json();
            this.renderStoriesPreview();
        } catch (error) {
            console.error('Erreur de chargement des stories:', error);
        }
    }

    renderStoriesPreview() {
        const container = document.querySelector('.stories-container');
        this.stories.forEach(story => {
            const storyElement = this.createStoryPreviewElement(story);
            container.appendChild(storyElement);
        });
    }

    createStoryPreviewElement(story) {
        const element = document.createElement('div');
        element.className = 'story-item';
        element.innerHTML = `
            <div class="story-avatar">
                <img src="${story.user.profile_picture}" alt="${story.user.username}">
            </div>
            <small>${story.user.username}</small>
        `;
        element.addEventListener('click', () => this.openStory(story));
        return element;
    }

    openStory(story) {
        this.currentStory = story;
        this.showStoryInModal();
    }

    showStoryInModal() {
        const modalContent = document.querySelector('#storyModal .modal-body');
        modalContent.innerHTML = `
            <div class="story-content">
                <div class="story-header">
                    <img src="${this.currentStory.user.profile_picture}" 
                         class="rounded-circle" width="32" height="32">
                    <span>${this.currentStory.user.username}</span>
                    <small>${this.getTimeAgo(this.currentStory.created_at)}</small>
                </div>
                <div class="story-media">
                    ${this.getStoryMedia()}
                </div>
            </div>
        `;
        this.modal.show();
    }

    getStoryMedia() {
        if (this.currentStory) {
            // Implémentation pour obtenir le média de la story
        }
        return '';
    }

    getTimeAgo(date) {
        // Implémentation pour obtenir le temps écoulé depuis la date donnée
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    const storiesManager = new StoriesManager();
}); 