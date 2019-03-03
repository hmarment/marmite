import React from 'react';

import Recipe from './Recipe';

const Feed = (props) => {
  return (
    <div>
      {
        props.recipes.map((recipe) => {
          return (
            <Recipe key={ recipe.id } recipe={ recipe } />
          );
        })
      }
    </div>
  )
};

export default Feed;
