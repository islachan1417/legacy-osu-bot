import { Button, Card, List, Modal, Space } from "antd";
import { IRoom, IRoomForm } from "../Interface";
import { deleteRoom, updateRoom } from "../api/RoomAPI";
import { useState } from "react";
import RoomForm from "./RoomForm";

export default function RoomCard(props: IRoom) {
  const room = props ?? {};
  const {
    name,
    bot_mode,
    play_mode,
    room_size,
    score_mode,
    team_mode,
    is_created,
    room_id,
    users,
    is_closed,
    is_connected,
    id,
  } = room ?? {};
  const [showModal, setShowModal] = useState(false);

  return (
    <List.Item>
      <Card
        title={
          <>
            {name}
            {" ~ "}
            <b>
              <span
                style={{
                  color: is_closed ? "gray" : is_connected ? "green" : "red",
                }}
              >
                {is_closed
                  ? "Closed"
                  : is_connected
                  ? "Connected"
                  : "Not Connected"}
              </span>
            </b>
          </>
        }
      >
        <div style={{ display: "flex", flexDirection: "column" }}>
          <span>
            <b>ID:</b> {id}
          </span>
          <span>
            <b>Room ID:</b> {room_id}
          </span>
          <span>
            <b>Bot:</b> {bot_mode}
          </span>
          <span>
            <b>Play:</b> {play_mode}
          </span>
          <span>
            <b>Score:</b> {score_mode}
          </span>
          <span>
            <b>Team:</b> {team_mode}
          </span>
          <span>
            <b>Size:</b> {room_size}
          </span>
          {users?.length ? (
            <span>
              <b>Users:</b> {users?.join(", ") ?? "None"}
            </span>
          ) : (
            <></>
          )}

          <Space wrap style={{ marginTop: 15 }}>
            <Button
              type="default"
              disabled={is_closed || !is_connected || !is_created}
              onClick={() => {
                setShowModal(true);
              }}
            >
              Update
            </Button>
            <Button
              type="primary"
              danger
              disabled={is_closed || !is_connected || !is_created}
              onClick={() => deleteRoom(id)}
            >
              Delete
            </Button>
          </Space>
        </div>
      </Card>
      <Modal
        title="Basic Modal"
        open={showModal}
        onOk={() => setShowModal(false)}
        onCancel={() => setShowModal(false)}
        footer={false}
      >
        <RoomForm
          onFinished={async (values: IRoomForm) => await updateRoom(values, id)}
          initialValues={room}
        />
      </Modal>
    </List.Item>
  );
}
