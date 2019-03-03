import React from 'react';

const Recipe = (props) => {
  return (
    <div key={ props.recipe.id }>
      <h4
        className="box title is-4"
      >{ props.recipe.name }
      </h4>
      <br/>
      <img src={ props.recipe.thumbnail } />
      <br/>
      <p> { props.recipe.body } </p>
    </div>
  );
};

export default Recipe;
