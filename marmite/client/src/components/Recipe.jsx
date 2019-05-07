import React from 'react';
import Card from 'react-bootstrap/Card'

const Recipe = (props) => {
  return (
    <div className="recipe" key={ props.recipe.id }>
      <Card className="mx-auto mt-3" style={{ width: '50rem' }}>
        <Card.Img src={ props.recipe.image } alt={ props.recipe.name }/>
        <Card.Body>
          <Card.Title> { props.recipe.name } </Card.Title>
          <Card.Text> { props.recipe.instructions } </Card.Text>
        </Card.Body>
      </Card>
    </div>
  );
};

export default Recipe;
