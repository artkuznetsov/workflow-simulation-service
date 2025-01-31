import React, { Component } from "react";

class Card extends Component {
  handleOnBlur = e => {
    this.props.onEditCard(e.target.value, this.props.id);
  };

  handleOnDragStart = e => {
    this.props.onDragCardStart(e, this.props.id);
  };

  handleOnDragEnd = e => {
    this.props.onDragCardEnd(e, this.props.id);
  };

  render() {
    return (
      <div
        className="card"
        style={this.props.isDragged ? { opacity: 0.3 } : { opacity: 1 }}
        draggable
        onDragStart={this.handleOnDragStart}
        onDragEnd={this.handleOnDragEnd}
      >
        <div className="card-body">
          <button
            className="btn-danger btn-sm"
            onClick={() => this.props.onDeleteCard(this.props.id)}
          />
          <div className="form-group" onBlur={this.handleOnBlur}>
            Type: {this.props.type}<br/>
            Assigned: {this.props.assigned_to}<br/>
            Status: {this.props.status}
            {/*<textarea*/}
            {/*  className="form-control"*/}
            {/*  rows="2"*/}
            {/*  defaultValue={this.props.content}*/}
            {/*/>*/}
          </div>
        </div>
      </div>
    );
  }
}
export default Card;
