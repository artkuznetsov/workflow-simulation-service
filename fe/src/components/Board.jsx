import React, { Component } from "react";
import List from "./List";
import API from "../api";

class Board extends Component {
  constructor(props) {
    super(props);

    this.api = API;


    this.state = {
      boardId: 1,
      columns: [],
      tickets: []
    };
  }

  componentWillReceiveProps(props) {
    const { refresh, id } = this.props;
    if (props.refresh !== refresh) {
      this.initialBoard(this.state.boardId)
    }
  }

  componentDidMount() {
    this.initialBoard(this.state.boardId);
  }

  handleCreateCard = listName => {
    this.props.store.dispatch({ type: "ADD_CARD", listName });
  };

  handleEditCard = (content, cardId) => {
    this.props.store.dispatch({ type: "EDIT_CARD", content, cardId });
  };

  handleDeleteCard = cardId => {
    this.props.store.dispatch({ type: "DELETE_CARD", cardId });
  };

  handleCreateList = () => {
    this.props.store.dispatch({ type: "ADD_LIST" });
  };

  handleEditList = (newListName, listName) => {
    this.props.store.dispatch({ type: "EDIT_LIST", newListName, listName });
  };

  handleDeleteList = listName => {
    this.props.store.dispatch({ type: "DELETE_LIST", listName });
  };

  handleOnDragCardStart = (e, id) => {
    this.props.store.dispatch({ type: "ON_DRAG_CARD_START", e, id });
  };

  handleOnDragCardEnd = (e, id) => {
    this.props.store.dispatch({ type: "ON_DRAG_CARD_END", e, id });
  };

  handleOnDropCard = (e, listName) => {
    this.props.store.dispatch({ type: "ON_DROP_CARD", e, listName });
  };

  handleOnDragListStart = (e, listName) => {
    this.props.store.dispatch({ type: "ON_DRAG_LIST_START", e, listName });
  };

  handleOnDragListEnd = (e, listName) => {
    this.props.store.dispatch({ type: "ON_DRAG_LIST_END", e, listName });
  };

  handleOnDropList = (e, listName) => {
    this.props.store.dispatch({ type: "ON_DROP_LIST", e, listName });
    this.props.store.dispatch({ type: "SORT_LISTS" });
  };

  initialBoard = (id) => {
    this.api.getBoard(id)
        .then(board => {
          const boardName = board.name;

          this.setState({boardId: board.id});

          this.props.store.dispatch({type: "BOARD_DISPLAY_NAME", boardName});

          this.api.getColumnsByBoardId(id)
              .then(res => {
                this.setState({columns: res.data});
                this.api.getTickets()
                    .then(tickets => this.setState({tickets: tickets}))
              })
        });
  };

  renderList = column => {
    const filtered_cards = this.state.tickets.filter(card => card.column_id === column.id);

    return (
      <List
        key={column.id}
        id={column.id}
        name={column.name}
        isDragged={column.isDragged}
        cards={filtered_cards}
        dragType={this.props.store.getState().dragType}
        onDeleteCard={this.handleDeleteCard}
        onEditCard={this.handleEditCard}
        onCreateCard={this.handleCreateCard}
        onDeleteList={this.handleDeleteList}
        onEditList={this.handleEditList}
        onDragCardStart={this.handleOnDragCardStart}
        onDragCardEnd={this.handleOnDragCardEnd}
        onDropCard={this.handleOnDropCard}
        onDragListStart={this.handleOnDragListStart}
        onDragListEnd={this.handleOnDragListEnd}
        onDropList={this.handleOnDropList}
        boardId={this.state.boardId}
      />
    );
  };

  render() {
    if (!this.state.boardId && !this.state.cards) {
      return "Can't define the board.";
    }
    return (
      <React.Fragment>
        <div className="container">
          <h1>
            {this.props.store.getState().boardName}
            {/*<button type="button" className="btn btn-primary" onClick={this.handleCreateList}>Add a list...</button>*/}
          </h1>
          <div className="row">
            {/*{this.props.store.getState().lists.map(this.renderList)}*/}
            {this.state.columns.map(this.renderList)}
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default Board;
