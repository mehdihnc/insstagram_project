function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

class PostInteractions {
    constructor() {
        this.setupLikeButtons();
        this.setupCommentForms();
    }

    setupLikeButtons() {
        document.querySelectorAll('.like-btn').forEach(button => {
            button.addEventListener('click', async (e) => {
                e.preventDefault();
                const postId = button.dataset.postId;
                await this.toggleLike(postId, button);
            });
        });
    }

    async toggleLike(postId, button) {
        try {
            const response = await fetch(`/interactions/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            });

            const data = await response.json();
            const icon = button.querySelector('i');
            const likesCount = button.closest('.card-body').querySelector('.likes-count');
            
            if (data.is_liked) {
                icon.classList.replace('far', 'fas');
            } else {
                icon.classList.replace('fas', 'far');
            }

            if (likesCount) {
                likesCount.textContent = `${data.likes_count} j'aime${data.likes_count !== 1 ? 's' : ''}`;
            }

        } catch (error) {
            console.error('Erreur lors du like:', error);
        }
    }

    setupCommentForms() {
        document.querySelectorAll('.comment-form').forEach(form => {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const postId = form.dataset.postId;
                const input = form.querySelector('input');
                const content = input.value.trim();
                
                if (content) {
                    await this.addComment(postId, content, form);
                }
            });
        });
    }

    async addComment(postId, content, form) {
        try {
            const response = await fetch(`/interactions/comment/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `content=${encodeURIComponent(content)}`
            });

            const data = await response.json();
            if (data.status === 'success') {
                const commentsSection = form.closest('.card-body').querySelector('.comments-section');
                commentsSection.insertAdjacentHTML('beforeend', `
                    <div class="comment mb-2">
                        <p class="mb-1">
                            <span class="fw-bold">${data.comment.username}</span>
                            ${data.comment.content}
                        </p>
                    </div>
                `);
                form.querySelector('input').value = '';
            }
        } catch (error) {
            console.error('Erreur lors de l\'ajout du commentaire:', error);
        }
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    new PostInteractions();
}); 