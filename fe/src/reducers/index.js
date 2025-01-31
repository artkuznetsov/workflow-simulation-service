const initialState = {
  // Init some cards for the exemple
  cards: [
    {
      id: 0,
      list: "Backlog",
      content: "Buy coffee for everyone",
      isDragged: false
    },
    { id: 1, list: "Backlog", content: "Contact Kaneoh", isDragged: false },
    {
      id: 2,
      list: "Backlog",
      content: "Improve website UI",
      isDragged: false
    },
    {
      id: 3,
      list: "Backlog",
      content: "Sales appointment",
      isDragged: false
    },
    {
      id: 4,
      list: "Backlog",
      content: "Hire a new manager",
      isDragged: false
    },
    {
      id: 5,
      list: "Backlog",
      content: "Create a new logo",
      isDragged: false
    },
    {
      id: 6,
      list: "Backlog",
      content: "Appointment with interns",
      isDragged: false
    },
    {
      id: 7,
      list: "Priorities",
      content: "Increase sales revenu by 30% in Q3",
      isDragged: false
    },
    {
      id: 8,
      list: "Priorities",
      content: "Launch first international expansion",
      isDragged: false
    },
    {
      id: 9,
      list: "Priorities",
      content: "Test new messaging for SMB market",
      isDragged: false
    },
    {
      id: 10,
      list: "Current",
      content: "Website Redesign",
      isDragged: false
    },
    { id: 11, list: "Current", content: "Ship iOS app", isDragged: false },
    { id: 12, list: "Current", content: "Analytics Data", isDragged: false },
    {
      id: 13,
      list: "Current",
      content: "Increase conversion rate by 20% by Q3",
      isDragged: false
    },
    {
      id: 14,
      list: "Current",
      content: "Develop Engineering Blog",
      isDragged: false
    },
    {
      id: 15,
      list: "Current",
      content: "Brand Guidelines",
      isDragged: false
    },
    {
      id: 16,
      list: "Completed",
      content: "Social Media Campaign",
      isDragged: false
    },
    {
      id: 17,
      list: "Completed",
      content: "Update Help Documentation",
      isDragged: false
    }
  ],
  lists: [
    { id: 0, name: "Backlog", order: 1, isDragged: false },
    { id: 1, name: "Priorities", order: 2, isDragged: false },
    { id: 2, name: "Current", order: 3, isDragged: false },
    { id: 3, name: "Completed", order: 4, isDragged: false }
  ],
  dragType: "none"
};

export default (state = initialState, action) => {
  let newState;
  switch (action.type) {
    case "STORE_CARDS_PER_COLUMN":
      newState = { ...state };
      action.cards.map(card => newState.cards.push(card));
      return newState;
    case "BOARD_DISPLAY_NAME":
      newState = { ...state };
      newState.boardName = action.boardName;
      return newState;
    case "SORT_LISTS":
      newState = { ...state };
      newState.lists.sort((a, b) => {
        if (Number(a.order) > Number(b.order)) {
          return 1;
        } else {
          return -1;
        }
      });
      return newState;
    case "ADD_CARD":
      newState = { ...state };
      newState.cards.push({
        id: state.cards.length,
        list: action.listName,
        content: "",
        isDragged: false
      });
      return newState;
    case "EDIT_CARD":
      newState = { ...state };
      newState.cards[action.cardId].content = action.content;
      return newState;
    case "DELETE_CARD":
      newState = { ...state };
      newState.cards = newState.cards.filter(c => c.id !== action.cardId);
      return newState;
    case "ADD_LIST":
      newState = { ...state };
      newState.lists.push({
        id: newState.lists.length,
        name: "",
        order: newState.lists.length + 1
      });
      return newState;
    case "EDIT_LIST":
      newState = { ...state };
      newState.lists.forEach(list => {
        if (list.name === action.listName) {
          list.name = action.newListName;
        }
      });
      newState.cards.forEach(card => {
        if (card.list === action.listName) {
          card.list = action.newListName;
        }
      });
      return newState;
    case "DELETE_LIST":
      newState = { ...state };
      newState.lists = newState.lists.filter(l => l.name !== action.listName);
      return newState;
    case "ON_DRAG_CARD_START":
      newState = { ...state };
      action.e.dataTransfer.setData("id", action.id);
      newState.cards[action.id].isDragged = true;
      newState.dragType = "card";
      return newState;
    case "ON_DRAG_CARD_END":
      newState = { ...state };
      action.e.dataTransfer.clearData();
      newState.cards[action.id].isDragged = false;
      newState.dragType = "none";
      return newState;
    case "ON_DROP_CARD":
      newState = { ...state };
      newState.dragType = "none";
      newState.cards.forEach(card => {
        if (Number(card.id) === Number(action.e.dataTransfer.getData("id"))) {
          card.list = action.listName;
          card.isDragged = false;
        }
      });
      action.e.dataTransfer.clearData();
      return newState;
    case "ON_DRAG_LIST_START":
      newState = { ...state };
      if (newState.dragType === "none") {
        newState.dragType = "list";
        newState.lists.forEach(list => {
          if (list.name === action.listName) {
            list.isDragged = true;
          }
        });
        action.e.dataTransfer.setData("name", action.listName);
      }
      return newState;
    case "ON_DRAG_LIST_END":
      newState = { ...state };
      action.e.dataTransfer.clearData();
      newState.dragType = "none";
      newState.lists.forEach(list => {
        if (list.name === action.listName) {
          list.isDragged = false;
        }
      });
      return newState;
    case "ON_DROP_LIST":
      newState = { ...state };
      let list1, list2;
      newState.lists.forEach(list => {
        if (list.name === action.listName) {
          list.isDragged = false;
          list1 = list;
        }
        if (list.name === String(action.e.dataTransfer.getData("name"))) {
          list2 = list;
        }
      });
        action.e.dataTransfer.clearData();
        let orderSave = list1.order;
        list1.order = list2.order;
        list2.order = orderSave;
      return newState;
    default:
      return state;
  }
};
