import axios from 'axios';

export default class RecipeService{

    listRecipes() {
        const url = `${process.env.REACT_APP_BACKEND_URL}/api/recipes/`;
        return axios.get(url).then(response => response.data);
    };
    getRecipe(id) {
        const url = `${process.env.REACT_APP_BACKEND_URL}/api/recipes/${id}`;
        return axios.get(url).then(response => response.data);
    };
    deleteRecipe(recipe){
        const url = `${process.env.REACT_APP_BACKEND_URL}/api/recipes/${recipe.id}`;
        return axios.delete(url);
    };
    createRecipe(recipe){
        const url = `${process.env.REACT_APP_BACKEND_URL}/api/recipes/`;
        return axios.post(url, recipe);
    };
    updateRecipe(recipe){
        const url = `${process.env.REACT_APP_BACKEND_URL}/api/recipes/${recipe.id}`;
        return axios.put(url, recipe);
    };
}