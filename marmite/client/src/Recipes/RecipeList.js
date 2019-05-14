import  React, { Component } from  'react';
import Recipe from '../components/Recipe';
import  RecipeService  from  './RecipeService';

const  recipeService  =  new  RecipeService();

class  RecipeList  extends  Component {

    constructor(props) {
        super(props);
        this.state = {
            recipes: [],
        };
    }

    componentDidMount() {
        // fetch recipes from backend and add to state properties
        recipeService.listRecipes().then((recipes) => {this.setState({ recipes: recipes});})  // new
        .catch((err) => { console.log(err); })
    }

    render() {
        return (
            <div>
            {
                this.state.recipes.map((recipe) => {
                return (
                    <Recipe key={ recipe.id } recipe={ recipe } />
                );
                })
            }
            </div>
        )
    }
}
export default RecipeList;