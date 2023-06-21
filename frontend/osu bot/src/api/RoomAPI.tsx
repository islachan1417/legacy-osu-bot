import { toast } from "react-toastify";
import { IRoomForm } from "../Interface";
import { CONFIG } from "../constants";

export async function createRoom(values: IRoomForm) {
  const res = await fetch(`${CONFIG.api}room`, {
    method: "POST",
    body: JSON.stringify(values),
    headers: {
      "content-type": "application/json",
    },
  });

  if (!res.ok) {
    toast("Submission Failed", {
      type: "error",
    });

    return false;
  }

  toast("Room Created");

  return true;
}

export async function deleteRoom(id: string) {
  const res = await fetch(`${CONFIG.api}/room/${id}`, {
    method: "delete",
  });

  if (!res.ok) {
    toast("Deletion Failed", {
      type: "error",
    });

    return;
  }

  toast("Deletion Success");
}

export async function updateRoom(values: IRoomForm, id: string) {
  const res = await fetch(`${CONFIG.api}/room/${id}`, {
    method: "put",
    body: JSON.stringify(values),
    headers: {
      "content-type": "application/json",
    },
  });

  if (!res.ok) {
    toast("Update Failed", {
      type: "error",
    });

    return false;
  }

  toast("Update Success");
  return true;
}
