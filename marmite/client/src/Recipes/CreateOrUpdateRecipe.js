import  React, { Component } from  'react';
import Recipe from '../components/Recipe';
import {Button, Col, Form} from 'react-bootstrap'

import  RecipeService  from  './RecipeService';

const  recipeService  =  new  RecipeService();

class  CreateOrUpdateRecipe  extends  Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleCreate(){
        recipeService.createRecipe(
            {
            "name":  this.refs.recipeName.value,
            "short_description":  this.refs.recipeShortDescription.value,
            "source": "self",
            "type": "self",
            "preparation_time":  this.refs.recipePreparationTime.value,
            "cooking_time":  this.refs.recipeCookingTime.value,
            "instructions":  this.refs.recipeInstructions.value,
            "image":  this.refs.recipeImageUrl.value
            }).then((result)=>{
                    alert("Recipe created!");
            }).catch(()=>{
                    alert('There was an error! Please re-check your form.');
            });
    }

    handleUpdate(id){
        recipeService.updateRecipe(
            {
            "id":  id,
            "name":  this.refs.recipeName.value,
            "short_description":  this.refs.recipeShortDescription.value,
            "source": "self",
            "type": "self",
            "preparation_time":  this.refs.recipePreparationTime.value,
            "cooking_time":  this.refs.recipeCookingTime.value,
            "instructions":  this.refs.recipeInstructions.value,
            "image":  this.refs.recipeImageUrl.value
            }
            ).then((result)=>{
        
                alert("Recipe updated!");
            }).catch(()=>{
                alert('There was an error! Please re-check your form.');
            });
        }

    handleSubmit(event) {
        const { match: { params } } =  this.props;
        if (params  &&  params.id){
            this.handleUpdate(params.id);
        }
        else
        {
            this.handleCreate();
        }
        event.preventDefault();
    }
    
    componentDidMount(){
        const { match: { params } } =  this.props;
        if (params  &&  params.id) {
            recipeService.getRecipe(params.id).then((r) => {
                this.refs.recipeName.value = r.name;
                this.refs.recipeShortDescription.value  =  r.short_description;
                this.refs.recipePreparationTime.value  =  r.preparation_time;
                this.refs.recipeCookingTime.value  =  r.cooking_time;
                this.refs.recipeInstructions.value  =  r.instructions;
                this.refs.recipeImageUrl.value  =  r.image;
            })
        }
    }

    render() {
        return (
            <div>
                <Form>
                    <Form.Group controlId="recipeName">
                        <Form.Label>Title</Form.Label>
                        <Form.Control type="text" placeholder="Name" ref="recipeName"/>
                    </Form.Group>
                    <Form.Group controlId="recipeShortDescription">
                        <Form.Label>Short Description</Form.Label>
                        <Form.Control type="textarea" rows="3" placeholder="Name" ref="recipeShortDescription"/>
                    </Form.Group>
                    <Form.Group controlId="recipeImageUrl">
                        <Form.Label>Image Url</Form.Label>
                        <Form.Control type="text" placeholder="Image Link" ref="recipeImageUrl"/>
                    </Form.Group>

                    <Form.Row>
                        <Form.Group as={Col} controlId="recipePreparationTime">
                        <Form.Label>Preparation Time</Form.Label>
                        <Form.Control ref="recipePreparationTime"/>
                        </Form.Group>

                        <Form.Group as={Col} controlId="recipeCookingTime">
                        <Form.Label>Cooking Time</Form.Label>
                        <Form.Control ref="recipeCookingTime"/>
                        </Form.Group>
                    </Form.Row>

                    <Form.Group controlId="recipeInstructions">
                        <Form.Label>Instructions</Form.Label>
                        <Form.Control type="textarea" rows="10" placeholder="Instructions" ref="recipeInstructions"/>
                    </Form.Group>

                    <Button variant="primary" type="submit">
                        Submit
                    </Button>
                    </Form>
            </div>
        )
    }

}
export default CreateOrUpdateRecipe;