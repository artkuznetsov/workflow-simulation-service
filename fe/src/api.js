import axios from 'axios';



class API{
    static getBoard(id){
        return axios.get(`http://localhost:5000/api/v1/board/${id}`).then(res => res.data[0])
    };

    static getColumnsByBoardId(boardId){
        return axios.get(`http://localhost:5000/api/v1/column?board=${boardId}`)
    }

    static getTicketsByColumnId(columnId){
        return axios.get(`http://localhost:5000/api/v1/ticket?column_id=${columnId}`).then(res => res.data)
    }

    static getTickets(){
        return axios.get(`http://localhost:5000/api/v1/ticket`).then(res => res.data)
    }
}

export default API;
