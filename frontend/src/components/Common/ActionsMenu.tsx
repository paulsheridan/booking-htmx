import {
  Button,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  useDisclosure,
} from "@chakra-ui/react";
import { BsThreeDotsVertical } from "react-icons/bs";
import { FiEdit, FiTrash } from "react-icons/fi";

import type {
  ClientPublic,
  UserPublic,
  ServicePublic,
  AppointmentPublic,
} from "../../client";
import EditUser from "../Admin/EditUser";
import EditClient from "../Clients/EditClient";
import EditService from "../Services/EditService";
import Delete from "./DeleteAlert";
import EditAppointment from "../Appointments/EditAppointment";

interface ActionsMenuProps {
  type: string;
  value: ClientPublic | UserPublic | ServicePublic;
  disabled?: boolean;
}

const ActionsMenu = ({ type, value, disabled }: ActionsMenuProps) => {
  const editUserModal = useDisclosure();
  const editClientModal = useDisclosure();
  const editServiceModal = useDisclosure();
  const editAppointmentModal = useDisclosure();
  const deleteModal = useDisclosure();

  return (
    <>
      <Menu>
        <MenuButton
          isDisabled={disabled}
          as={Button}
          rightIcon={<BsThreeDotsVertical />}
          variant="unstyled"
        />
        <MenuList>
          <MenuItem
            onClick={editUserModal.onOpen}
            icon={<FiEdit fontSize="16px" />}
          >
            Edit {type}
          </MenuItem>
          <MenuItem
            onClick={deleteModal.onOpen}
            icon={<FiTrash fontSize="16px" />}
            color="ui.danger"
          >
            Delete {type}
          </MenuItem>
        </MenuList>
        {type === "User" ? (
          <EditUser
            user={value as UserPublic}
            isOpen={editUserModal.isOpen}
            onClose={editUserModal.onClose}
          />
        ) : type === "Client" ? (
          <EditClient
            client={value as ClientPublic}
            isOpen={editClientModal.isOpen}
            onClose={editClientModal.onClose}
          />
        ) : type === "Service" ? (
          <EditService
            service={value as ServicePublic}
            isOpen={editServiceModal.isOpen}
            onClose={editServiceModal.onClose}
          />
        ) : (
          <EditAppointment
            appointment={value as AppointmentPublic}
            isOpen={editAppointmentModal.isOpen}
            onClose={editAppointmentModal.onClose}
          />
        )}
        <Delete
          type={type}
          id={value.id}
          isOpen={deleteModal.isOpen}
          onClose={deleteModal.onClose}
        />
      </Menu>
    </>
  );
};

export default ActionsMenu;
