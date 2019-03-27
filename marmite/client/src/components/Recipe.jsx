import React from 'react';
import Card from 'react-bootstrap/Card'

const Recipe = (props) => {
  return (
    <div className="recipe" key={ props.recipe.id }>
      <Card className="mx-auto mt-3" style={{ width: '50rem' }}>
        <Card.Img src={ props.recipe.thumbnail } alt={ props.recipe.web_title }/>
        <Card.Body>
          <Card.Title> { props.recipe.web_title } </Card.Title>
          <Card.Text> { props.recipe.body } </Card.Text>
        </Card.Body>
      </Card>
    </div>
  );
};

export default Recipe;
