class Api {
  constructor(url, headers) {
    this._url = url;
    this._headers = headers;
  }

  _getAuthHeaders() {
    const token = localStorage.getItem('access');
    return token ? { Authorization: `Token ${token}` } : {};
  }

  refreshToken() {
    // Для простых токенов нет refresh, просто возвращаем ошибку
    return Promise.reject(new Error('Token refresh not supported'));
  }

  checkResponse(res) {
    return new Promise((resolve, reject) => {
      if (res.status === 204) {
        return resolve(res);
      }
      if (res.status === 401) {
        // Token expired, try to refresh
        return this.refreshToken()
          .then(() => {
            // Retry the original request
            const originalRequest = res.url;
            return fetch(originalRequest, {
              ...res,
              headers: {
                ...this._headers,
                ...this._getAuthHeaders(),
              },
            }).then(this.checkResponse);
          })
          .catch((error) => {
            // If refresh failed, redirect to login
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            window.location.href = '/signin';
            return reject(error);
          });
      }
      const func = res.status < 400 ? resolve : reject;
      res.json().then((data) => func(data));
    });
  }

  checkFileDownloadResponse(res) {
    return new Promise((resolve, reject) => {
      if (res.status < 400) {
        return res.blob().then((blob) => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "shopping-list";
          document.body.appendChild(a);
          a.click();
          a.remove();
        });
      }
      reject();
    });
  }

  signin({ email, password }) {
    return fetch("/api/auth/token/login/", {
      method: "POST",
      headers: this._headers,
      body: JSON.stringify({
        email,
        password,
      }),
    }).then(this.checkResponse);
  }

  signout() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    return Promise.resolve();
  }

  signup({ email, password, username, first_name, last_name }) {
    return fetch(`/api/users/`, {
      method: "POST",
      headers: this._headers,
      body: JSON.stringify({
        email,
        password,
        username,
        first_name,
        last_name,
      }),
    }).then(this.checkResponse);
  }

  getUserData() {
    return fetch(`/api/users/me/`, {
      method: "GET",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkResponse);
  }

  changePassword({ current_password, new_password }) {
    return fetch(`/api/users/set_password/`, {
      method: "POST",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
      body: JSON.stringify({ current_password, new_password }),
    }).then(this.checkResponse);
  }

  changeAvatar({ file }) {
    return fetch(`/api/users/me/avatar/`, {
      method: "PUT",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
      body: JSON.stringify({ avatar: file }),
    }).then(this.checkResponse);
  }

  deleteAvatar() {
    return fetch(`/api/users/me/avatar/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkResponse);
  }

  resetPassword({ email }) {
    return fetch(`/api/users/reset_password/`, {
      method: "POST",
      headers: this._headers,
      body: JSON.stringify({ email }),
    }).then(this.checkResponse);
  }

  getRecipes({
    page = 1,
    limit = 6,
    is_favorited = 0,
    is_in_shopping_cart = 0,
    author
  } = {}) {
    return fetch(
      `/api/recipes/?page=${page}&limit=${limit}${
        author ? `&author=${author}` : ""
      }${is_favorited ? `&is_favorited=${is_favorited}` : ""}${
        is_in_shopping_cart ? `&is_in_shopping_cart=${is_in_shopping_cart}` : ""
      }`,
      {
        method: "GET",
        headers: {
          ...this._headers,
          ...this._getAuthHeaders(),
        },
      }
    ).then(this.checkResponse);
  }

  getRecipe({ recipe_id }) {
    return fetch(`/api/recipes/${recipe_id}/`, {
      method: "GET",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkResponse);
  }

  createRecipe({
    name = "",
    image,
    cooking_time = 0,
    text = "",
    ingredients = [],
  }) {
    return fetch("/api/recipes/", {
      method: "POST",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
      body: JSON.stringify({
        name,
        image,
        cooking_time,
        text,
        ingredients,
      }),
    }).then(this.checkResponse);
  }

  updateRecipe(
    { name, recipe_id, image, cooking_time, text, ingredients },
    wasImageUpdated
  ) {
    return fetch(`/api/recipes/${recipe_id}/`, {
      method: "PATCH",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
      body: JSON.stringify({
        name,
        id: recipe_id,
        image: wasImageUpdated ? image : undefined,
        cooking_time: Number(cooking_time),
        text,
        ingredients,
      }),
    }).then(this.checkResponse);
  }

  addToFavorites({ id }) {
    return fetch(`/api/recipes/${id}/favorite/`, {
      method: "POST",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkResponse);
  }

  removeFromFavorites({ id }) {
    return fetch(`/api/recipes/${id}/favorite/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkResponse);
  }

  copyRecipeLink({ id }) {
    return fetch(`/api/recipes/${id}/get-link/`, {
      method: "GET",
      headers: this._headers,
    }).then(this.checkResponse);
  }

  getUser({ id }) {
    return fetch(`/api/users/${id}/`, {
      method: "GET",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkResponse);
  }

  getUsers({ page = 1, limit = 6 }) {
    return fetch(`/api/users/?page=${page}&limit=${limit}`, {
      method: "GET",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkResponse);
  }

  getSubscriptions({ page, limit = 6, recipes_limit = 3 }) {
    return fetch(
      `/api/users/subscriptions/?page=${page}&limit=${limit}&recipes_limit=${recipes_limit}`,
      {
        method: "GET",
        headers: {
          ...this._headers,
          ...this._getAuthHeaders(),
        },
      }
    ).then(this.checkResponse);
  }

  deleteSubscriptions({ author_id }) {
    return fetch(`/api/users/${author_id}/subscribe/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkResponse);
  }

  subscribe({ author_id }) {
    return fetch(`/api/users/${author_id}/subscribe/`, {
      method: "POST",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkResponse);
  }

  getIngredients({ name }) {
    return fetch(`/api/ingredients/?name=${name}`, {
      method: "GET",
      headers: this._headers,
    }).then(this.checkResponse);
  }

  addToOrders({ id }) {
    return fetch(`/api/recipes/${id}/shopping_cart/`, {
      method: "POST",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkResponse);
  }

  removeFromOrders({ id }) {
    return fetch(`/api/recipes/${id}/shopping_cart/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkResponse);
  }

  deleteRecipe({ recipe_id }) {
    return fetch(`/api/recipes/${recipe_id}/`, {
      method: "DELETE",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkResponse);
  }

  downloadFile() {
    return fetch(`/api/recipes/download_shopping_cart/`, {
      method: "GET",
      headers: {
        ...this._headers,
        ...this._getAuthHeaders(),
      },
    }).then(this.checkFileDownloadResponse);
  }
}

export default new Api(process.env.API_URL || "http://localhost", {
  "content-type": "application/json",
});